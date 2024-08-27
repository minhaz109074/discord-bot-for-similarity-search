from PIL import Image
import cv2
import numpy as np
from imgbeddings import imgbeddings
from PIL import Image
import psycopg2
import os

cascade_path = 'E:/astha it/Python-discord-bot/models/haarcascade_frontalface_default.xml'

def detect_faces_and_get_embedding(image_input, cascade_path = cascade_path):
    haar_cascade = cv2.CascadeClassifier(cascade_path)
    
    if isinstance(image_input, Image.Image):
        img = np.array(image_input.convert('L')) 
    elif isinstance(image_input, np.ndarray):
        img = cv2.cvtColor(image_input, cv2.COLOR_BGR2GRAY) 
    else:
        img = cv2.imread(image_input, cv2.IMREAD_GRAYSCALE) 
    
    if img is None:
        return None
    
    faces = haar_cascade.detectMultiScale(
        img,
        scaleFactor=1.03,
        minNeighbors=4,
        minSize=(200, 200)
    )
    
    if len(faces) == 0:
        return None
    
    x, y, w, h = faces[0]
    cropped_image = img[y : y + h, x : x + w]
    
    pil_img = Image.fromarray(cropped_image)
    
    ibed = imgbeddings()
    embedding = ibed.to_embeddings(pil_img)[0]
    
    return embedding

def detect_faces_and_save_image(image_path, output_path, cascade_path):
    haar_cascade = cv2.CascadeClassifier(cascade_path)
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    if img is None:
        print(f"Error: Unable to load image {image_path}")
        return False
    
    faces = haar_cascade.detectMultiScale(
        img,
        scaleFactor=1.03,
        minNeighbors=4,
        minSize=(200, 200)
    )
    
    if len(faces) == 0:
        print(f"No faces detected in {image_path}.")
        return False
    
    for x, y, w, h in faces:
        cropped_image = img[y : y + h, x : x + w]
        cv2.imwrite(output_path, cropped_image)
        print(f"Face detected and saved to {output_path}")
        
        pil_img = Image.fromarray(cropped_image)
        
        ibed = imgbeddings()
        embedding = ibed.to_embeddings(pil_img)[0]
        
        store_embedding_in_db(image_path, embedding)
        return True

def store_embedding_in_db(file_name, embedding):
    try:
        conn = psycopg2.connect(
            dbname="vector_image_db",
            user="postgres",
            password="12345",
            host="localhost", 
            port="5432" 
        )
        cur = conn.cursor()
        cur.execute('INSERT INTO pictures (picture, embedding) VALUES (%s, %s)', (file_name, embedding.tolist()))
        conn.commit()
        print(f"Embedding for {file_name} stored in database.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def find_similar_images(embedding, top_n=2, max_distance=0.1):
    try:
        conn = psycopg2.connect(
            dbname="vector_image_db",
            user="postgres",
            password="12345",
            host="localhost",  
            port="5432" 
        )
        cur = conn.cursor()

        string_representation = "[" + ",".join(map(str, embedding.tolist())) + "]"
        
        cur.execute("""
            SELECT picture, 1 - (embedding <=> %s) AS cosine_distance
            FROM pictures
            WHERE 1 - (embedding <=> %s) >= %s
            ORDER BY cosine_distance DESC
            LIMIT %s;
        """, (string_representation, string_representation, 1 - max_distance, top_n))
        
        rows = cur.fetchall()
        
        similar_images = []
        
        for row in rows:
            image_path = row[0]
            distance = row[1]
            similar_images.append(image_path)
            print(f"Image: {image_path}, Distance: {distance}")
        
        return similar_images
    
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()


def process_directory(directory_path, cascade_path):
    for filename in os.listdir(directory_path):
        if filename.endswith((".jpeg", ".jpg", ".png")):
            image_path = os.path.join(directory_path, filename)
            output_path = os.path.join("output/", f"output_{filename}")
            if detect_faces_and_save_image(image_path, output_path, cascade_path):
                print(f"Processed {filename}")
            else:
                print(f"Skipped {filename}")

