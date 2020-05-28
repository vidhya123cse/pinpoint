import dlib, cv2
import numpy as np


detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('models/shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('models/dlib_face_recognition_resnet_model_v1.dat')
#dnnFaceDetector = dlib.cnn_face_detection_model_v1("models/mmod_human_face_detector.dat")



def find_faces(img):
    dets = detector(img, 1)

    if len(dets) == 0:
        return np.empty(0), np.empty(0), np.empty(0)
    
    rects, shapes = [], []
    shapes_np = np.zeros((len(dets), 68, 2), dtype=np.int)
    for k, d in enumerate(dets):
        rect = ((d.left(), d.top()), (d.right(), d.bottom()))
        rects.append(rect)

        shape = sp(img, d)
        
        # convert dlib shape to numpy array
        for i in range(0, 68):
            shapes_np[k][i] = (shape.part(i).x, shape.part(i).y)

        shapes.append(shape)
        
    return rects, shapes, shapes_np





def encode_faces(img, shapes):
    face_descriptors = []
    for shape in shapes:
        face_descriptor = facerec.compute_face_descriptor(img, shape)
        face_descriptors.append(np.array(face_descriptor))

    return np.array(face_descriptors)




def define():

  img_paths = {
      'vidhya': 'img/vidhya.jpeg',
      'sabna': 'img/sabna.jpeg',
      'surya':'img/surya.jpg',
      'lakshmi':'img/lakshmi.jpeg',
      'mohanlal':'img/mohanlal.jpg',
      'obama' : 'img/bobama.jpg',
      'Mohanlal' : 'img/john.jpeg',
      'MohanLal':'img/john2.jpg'
  }

  descs = {
      'vidhya': None,
      'sabna': None,
      'surya': None,
      'lakshmi': None,
      'mohanlal': None,
      'Mohanlal': None,
      'MohanLal': None,
      'obama': None
  }

  for name, img_path in img_paths.items():
      img_bgr = cv2.imread(img_path)
      img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

      _, img_shapes, _ = find_faces(img_rgb)
      descs[name] = encode_faces(img_rgb, img_shapes)[0]

  np.save('img/descs.npy', descs)









define()
descs = np.load('img/descs.npy',allow_pickle=True)[()]



video_path = 0
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
  exit()

_, img_bgr = cap.read() # (800, 1920, 3)
padding_size = 0
resized_width = 1920
video_size = (resized_width, int(img_bgr.shape[0] * resized_width // img_bgr.shape[1]))
output_size = (resized_width, int(img_bgr.shape[0] * resized_width // img_bgr.shape[1] + padding_size * 2))

fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
writer = cv2.VideoWriter('%s_output.mp4' % (video_path.split('.')[0]), fourcc, cap.get(cv2.CAP_PROP_FPS), output_size)

while True:
  ret, img_bgr = cap.read()
  if not ret:
    break

  img_bgr = cv2.resize(img_bgr, video_size)
  img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

  # img_bgr = cv2.copyMakeBorder(img_bgr, top=padding_size, bottom=padding_size, left=0, right=0, borderType=cv2.BORDER_CONSTANT, value=(0,0,0))
  
  dets = detector(img_bgr, 1)

  for k, d in enumerate(dets):
    shape = sp(img_rgb, d)
    face_descriptor = facerec.compute_face_descriptor(img_rgb, shape)

    last_found = {'name': 'unknown', 'dist': 0.45, 'color': (0,0,255)}

    for name, saved_desc in descs.items():
      dist = np.linalg.norm([face_descriptor] - saved_desc, axis=1)

      if dist < last_found['dist']:
        last_found = {'name': name, 'dist': dist, 'color': (255,255,255)}

    cv2.rectangle(img_bgr, pt1=(d.left(), d.top()), pt2=(d.right(), d.bottom()), color=last_found['color'], thickness=2)
    cv2.putText(img_bgr, last_found['name'], org=(d.left(), d.top()), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=last_found['color'], thickness=2)

  writer.write(img_bgr)

  cv2.imshow('img', img_bgr)
  if cv2.waitKey(1) == ord('q'):
    break

cap.release()
writer.release()
