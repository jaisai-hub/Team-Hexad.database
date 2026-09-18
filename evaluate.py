import os
import numpy as np
import torch

from model import UNet
from dataset import test_images


IMAGE_DIR = "dataset/images"
MASK_DIR = "dataset/masks"

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("Device:", device)


model = UNet().to(device)

model.load_state_dict(
    torch.load(
        "oil_spill_unet.pth",
        map_location=device
    )
)

model.eval()


dice_scores = []
iou_scores = []
precision_scores = []
recall_scores = []


for image_name in test_images:

    image_path = os.path.join(
        IMAGE_DIR,
        image_name
    )

    mask_path = os.path.join(
        MASK_DIR,
        image_name
    )

    image = np.load(image_path)
    actual_mask = np.load(mask_path)

    input_tensor = torch.tensor(
        image,
        dtype=torch.float32
    ).unsqueeze(0).to(device)


    with torch.no_grad():

        output = model(input_tensor)

        probability = torch.sigmoid(output)

        prediction = (
            probability > 0.5
        ).float()


    prediction = (
        prediction
        .squeeze()
        .cpu()
        .numpy()
        .astype(np.uint8)
    )


    actual_mask = actual_mask.astype(np.uint8)


    intersection = (
        prediction * actual_mask
    ).sum()

    union = (
        prediction
        + actual_mask
        - prediction * actual_mask
    ).sum()


    true_positive = intersection

    false_positive = (
        (prediction == 1)
        & (actual_mask == 0)
    ).sum()

    false_negative = (
        (prediction == 0)
        & (actual_mask == 1)
    ).sum()


    dice = (
        2 * intersection
    ) / (
        prediction.sum()
        + actual_mask.sum()
        + 1e-6
    )


    iou = (
        intersection
    ) / (
        union + 1e-6
    )


    precision = (
        true_positive
    ) / (
        true_positive
        + false_positive
        + 1e-6
    )


    recall = (
        true_positive
    ) / (
        true_positive
        + false_negative
        + 1e-6
    )


    dice_scores.append(dice)
    iou_scores.append(iou)
    precision_scores.append(precision)
    recall_scores.append(recall)


    print(
        f"{image_name} | "
        f"Dice: {dice:.4f} | "
        f"IoU: {iou:.4f} | "
        f"Precision: {precision:.4f} | "
        f"Recall: {recall:.4f}"
    )


print("\n========== FINAL RESULTS ==========")

print(
    "Average Dice:",
    f"{np.mean(dice_scores):.4f}"
)

print(
    "Average IoU:",
    f"{np.mean(iou_scores):.4f}"
)

print(
    "Average Precision:",
    f"{np.mean(precision_scores):.4f}"
)

print(
    "Average Recall:",
    f"{np.mean(recall_scores):.4f}"
)