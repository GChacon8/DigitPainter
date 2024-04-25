import os
from PIL import Image
import torch
from torchvision import transforms

def load_images_from_dir(directory):
    images = []
    value =[]
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".png"):
                file_path = os.path.join(root, file)
                image = Image.open(file_path)
                images.append(image)
                value.append(int(file[0]))
    return (images,value)

def images_to_tensor(data):
    transform = transforms.Compose([  # Assuming images are resized to (224, 224)
        transforms.ToTensor(),
    ])
    images=data[0]
    labels=data[1]
    tensor_images = torch.stack([torch.flatten(transform(img)) for img in images])
    tensor_values = torch.tensor(labels)
    return (tensor_images, tensor_values)

# Change 'path_to_your_directory' to the actual directory containing your images
directory_path = 'Imagenes'
image_list = load_images_from_dir(directory_path)
tensor_data,tensor_label = images_to_tensor(image_list)
torch.save(tensor_data,"Data.pt")
torch.save(tensor_label,"Labels.pt")
print("Tensor shape:", tensor_data.shape)
