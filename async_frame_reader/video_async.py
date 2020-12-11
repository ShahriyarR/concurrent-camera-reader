def read_frame(capture):
    # The method for using OpenCV grab() - retrieve()
    # We are not using read() here because, documentation insists that it is slower in multi-thread environment.
    capture.grab()
    ret, frame = capture.retrieve()
    print(frame)
    if not ret:
        print("empty frame")
        return
    return frame
