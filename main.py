"""HAR-BAS main pipeline. Run:  python main.py"""
import os, datetime
import cv2
import numpy as np

import config
import os, datetime, time
from src.detector import Detector
from src.tracker import StepTracker
from src.conditions import ConditionChecker
from src.tts_alerts import TTSAlerts
from src.logger import EventLogger
from src.camera import CameraSystem
from src.gui import MonitorGUI

N_STEPS  = len(config.EXPERIMENT_STEPS)
IDS      = list(range(N_STEPS))          # step ids = indices
EXPECTED = 0                              # next expected step index

def draw_overlay(frame, res, texts):
    for label, (x1, y1, x2, y2, c) in res["objects"].items():
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 200, 0), 2)
        cv2.putText(frame, f"{label} {c:.2f}", (int(x1), int(y1) - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 0), 2)
    for (wx, wy) in res["wrists"]:
        cv2.circle(frame, (int(wx), int(wy)), 6, (0, 0, 255), -1)
    y = 30
    for txt, col in texts:
        cv2.putText(frame, txt, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, col, 2)
        y += 32
    return frame

def run():
    global EXPECTED
    done = []
    wanted = {o for c in config.STEP_CONDITIONS for o in c["objects"]}

    detector = Detector(config.POSE_MODEL, config.ROBOFLOW_API_KEY,
                        config.ROBOFLOW_MODEL_ID, config.CONF_THRES)
    tracker  = StepTracker([{"id": i} for i in IDS],
                           config.CONFIRM_FRAMES, config.COOLDOWN_FRAMES)
    checker  = ConditionChecker(config.STEP_CONDITIONS, config.DIST_THRESH,
                                config.SEPARATION_DIST, config.MOTION_THRESH,
                                config.PROXIMITY_DIST)
    tts      = TTSAlerts(config.ALERT_COOLDOWN)
    log      = EventLogger(config.LOGS_DIR)

    vpath = os.path.join(config.VIDEOS_DIR,
        f"exp_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4") if config.RECORD_LOCAL else None
    cam = CameraSystem(config.CAMERA_INDEX, config.FRAME_WIDTH, config.FRAME_HEIGHT,
                       None, 5000, vpath)
    gui = MonitorGUI()
    gui.set_experiment("BAS 5-Step Protocol")
    log.log("experiment_start", steps=config.EXPERIMENT_STEPS)

    frame_n = 0
    persist = {}  
    last_ooo_alert = 0.0   # object label -> [box, ttl_frames]
    last_res = {"wrists": [], "objects": {}}
    try:
        while True:
            frame = cam.read()
            if frame is None:
                continue
            frame_n += 1
            if frame_n % 2 == 0:
                new_res = detector.detect(frame, wanted_objects=wanted)
                for label, box in new_res["objects"].items():
                    persist[label] = [box, 20]      # keep last box ~1.5s
                for label in list(persist):
                    persist[label][1] -= 1
                    if persist[label][1] <= 0:
                        del persist[label]
                res = {"wrists": new_res["wrists"],
                       "objects": {k: v[0] for k, v in persist.items()}}
            else:
                res = {"wrists": last_res["wrists"], "objects": dict(last_res["objects"])}
            last_res = res

            active = None
            ooo_step = None
            if EXPECTED < N_STEPS and checker.active_step(EXPECTED, res):
                active = EXPECTED
            else:
                for i in IDS:
                    if i in done or i != EXPECTED + 1:
                        continue
                    if checker.active_step(i, res):
                        ooo_step = i
                        break
            if ooo_step is not None and done and (time.time() - last_ooo_alert > 5):
                last_ooo_alert = time.time()
                msg = f"Out of sequence: {config.EXPERIMENT_STEPS[ooo_step]}"
                tts.out_of_order(msg)
                gui.set_status("OUT OF SEQUENCE", "red")
                gui.log(msg)
                log.log("out_of_order", step=ooo_step)

            nxt = config.EXPERIMENT_STEPS[EXPECTED] if EXPECTED < N_STEPS else "ALL DONE"
            texts = [(f"Next: {nxt}", (255, 200, 0)),
                     (f"Progress: {len(done)}/{N_STEPS}", (0, 255, 255))]
            gui.set_next(nxt)
            gui.set_progress(f"{len(done)}/{N_STEPS}")
            if frame_n % 30 == 0:
                print(f"[DBG] objs={list(res['objects'].keys())} "
                      f"wrists={len(res['wrists'])} active={active} expected={EXPECTED}")

            confirmed = tracker.update(active)
            if confirmed is not None:
                checker.on_confirmed(confirmed)
                if confirmed == EXPECTED:
                    done.append(confirmed)
                    name = config.EXPERIMENT_STEPS[confirmed]
                    EXPECTED = confirmed + 1
                    tts.step_done(name)
                    gui.set_status(f"{name} confirmed", "green")
                    gui.log(f"Step confirmed: {name}")
                    log.log("step_confirmed", step=confirmed, name=name)
                    if EXPECTED < N_STEPS:
                        tts.next_step(config.EXPERIMENT_STEPS[EXPECTED])
                    else:
                        tts.experiment_complete()
                        gui.set_status("EXPERIMENT COMPLETE", "green")
                        log.log("experiment_complete")
                elif confirmed > EXPECTED:
                    skipped = config.EXPERIMENT_STEPS[EXPECTED:confirmed]
                    done.extend(range(EXPECTED, confirmed + 1))
                    msg = f"Step missed: {', '.join(skipped)}"
                    tts.step_skipped(msg)
                    gui.set_status("STEP MISSED", "red")
                    gui.log(msg)
                    log.log("step_skipped", skipped=skipped)
                    EXPECTED = confirmed + 1
                else:
                    msg = f"Out of order: {config.EXPERIMENT_STEPS[confirmed]}"
                    tts.out_of_order(msg)
                    gui.set_status("OUT OF SEQUENCE", "red")
                    gui.log(msg)
                    log.log("out_of_order", step=confirmed)

            frame = draw_overlay(frame, res, texts)
            gui.show_frame(frame)
    except KeyboardInterrupt:
        pass
    finally:
        log.log("experiment_end", progress=f"{len(done)}/{N_STEPS}")
        cam.release()
        gui.close()

if __name__ == "__main__":
    run()