import threading
import cv2
import streamlit as st
from streamlit_webrtc import webrtc_streamer

st.set_page_config(page_title="Webcam", layout="wide")
       

col1, col2 = st.columns(2)

lock = threading.Lock()
img_container = {"img": None}


def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    with lock:
        img_container["img"] = img
    return

with col1:
    ctx = webrtc_streamer(key="example", 
                          video_frame_callback=video_frame_callback,

                        #   rtc_configuration={  # Add this config
                        #     "iceServers": [
                        #         {"urls": ["turn:openrelay.metered.ca:443"],
                        #          "username": "openrelayproject",
                        #          "credential": "openrelayproject"
                        #          }
                        #         ]
                        #     },
                        rtc_configuration={
                                'iceServers': [
                                    {
                                    'url': 'stun:stun.l.google.com:19302'
                                    },
                                    {
                                    'url': 'turn:192.158.29.39:3478?transport=udp',
                                    'credential': 'JZEOEt2V3Qb0y27GRntt2u2PAYA=',
                                    'username': '28224511:1379330808'
                                    },
                                    {
                                    'url': 'turn:192.158.29.39:3478?transport=tcp',
                                    'credential': 'JZEOEt2V3Qb0y27GRntt2u2PAYA=',
                                    'username': '28224511:1379330808'
                                    }
                                ]
                                },
                          media_stream_constraints={"video": True, "audio": False})

imgout_place = col2.empty()

while ctx.state.playing:
    with lock:
        img = img_container["img"]
    if img is None:
        continue
    # Phát hiện khuôn mặt sẽ đặt ở đây
    # Kết quả trả về là imgout có đóng khung khuôn mặt
    imgout = cv2.flip(img, 0)

    imgout_place.image(imgout, channels='BGR')