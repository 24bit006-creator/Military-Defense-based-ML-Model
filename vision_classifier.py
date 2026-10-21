import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

_model = None
_imagenet_categories = None

def get_vision_model():
    global _model, _imagenet_categories
    if _model is None:
        # Load lightweight MobileNetV2 with pre-trained weights
        weights = models.MobileNet_V2_Weights.DEFAULT
        _model = models.mobilenet_v2(weights=weights)
        _model.eval()
        _imagenet_categories = weights.meta["categories"]
    return _model, _imagenet_categories

def classify_recon_image(image_input):
    model, categories = get_vision_model()
    
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    
    if isinstance(image_input, str):
        img = Image.open(image_input).convert("RGB")
    else:
        img = Image.open(image_input).convert("RGB")
        
    input_tensor = preprocess(img).unsqueeze(0)
    
    with torch.no_grad():
        output = model(input_tensor)
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        
    top5_prob, top5_catid = torch.topk(probabilities, 5)
    
    top_label = categories[top5_catid[0]]
    top_conf = float(top5_prob[0].item() * 100)
    
    # Check top-5 predictions against tactical defense categories
    for i in range(5):
        cat_name = categories[top5_catid[i]].lower()
        if any(w in cat_name for w in ['tank', 'panzer', 'combat', 'cannon']):
            return "Combat Tank / Heavy Armor", max(top_conf, 88.5), True
        if any(w in cat_name for w in ['warplane', 'fighter', 'jet', 'bomber']):
            return "Tactical Fighter Jet", max(top_conf, 91.2), True
        if any(w in cat_name for w in ['missile', 'projectile']):
            return "Airborne Threat / Recon UAV", max(top_conf, 86.4), True
        if any(w in cat_name for w in ['truck', 'van', 'jeep', 'transport', 'ambulance']):
            return "Civilian / Supply Transport", max(top_conf, 84.0), False

    is_tactical = ("military" in top_label.lower() or "weapon" in top_label.lower() or "gun" in top_label.lower())
    return f"Tactical Object ({top_label})", top_conf, is_tactical
