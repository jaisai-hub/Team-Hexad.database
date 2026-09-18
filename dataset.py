import os
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split


class OilSpillDataset(Dataset):

    def __init__(self, image_dir, mask_dir, image_names):
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.images = image_names

    def __len__(self):
        return len(self.images)

    def __getitem__(self, index):

        image_name = self.images[index]

        image_path = os.path.join(self.image_dir, image_name)
        mask_path = os.path.join(self.mask_dir, image_name)

        image = np.load(image_path)
        mask = np.load(mask_path)

        image = torch.tensor(image, dtype=torch.float32)
        mask = torch.tensor(mask, dtype=torch.float32)

        mask = mask.unsqueeze(0)

        return image, mask


image_dir = "dataset/images"
mask_dir = "dataset/masks"


all_images = sorted([
    f for f in os.listdir(image_dir)
    if f.endswith(".npy")
])


train_images, test_images = train_test_split(
    all_images,
    test_size=10,
    random_state=42,
    shuffle=True
)


print("Total images:", len(all_images))
print("Training images:", len(train_images))
print("Testing images:", len(test_images))


train_dataset = OilSpillDataset(
    image_dir,
    mask_dir,
    train_images
)

test_dataset = OilSpillDataset(
    image_dir,
    mask_dir,
    test_images
)


train_loader = DataLoader(
    train_dataset,
    batch_size=4,
    shuffle=True
)

test_loader = DataLoader(
    test_dataset,
    batch_size=4,
    shuffle=False
)


train_images_batch, train_masks_batch = next(iter(train_loader))

test_images_batch, test_masks_batch = next(iter(test_loader))


print("Training batch image shape:", train_images_batch.shape)
print("Training batch mask shape:", train_masks_batch.shape)

print("Testing batch image shape:", test_images_batch.shape)
print("Testing batch mask shape:", test_masks_batch.shape)