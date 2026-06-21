import httpx
import os
from PIL import Image, ImageFilter, ImageEnhance
from app.config import settings


STYLE_PROMPTS = {
    "anime": "Transform this image into Japanese anime style with vibrant colors, clean outlines, and cel-shading effect",
    "oil_painting": "Apply classical oil painting effect with thick brushstrokes, rich textures, and warm tones",
    "sketch": "Convert this image into a detailed pencil sketch with soft shading and delicate lines",
    "watercolor": "Apply watercolor painting effect with soft blending, pastel colors, and flowing washes",
    "pixel_art": "Convert this image into pixel art style with a retro 8-bit aesthetic and vibrant colors",
}


def resize_if_needed(image_path: str, max_dimension: int = None) -> Image.Image:
    """打开图片并按需等比缩放，避免过大图片消耗过多资源"""
    img = Image.open(image_path).convert("RGB")
    max_dim = max_dimension or settings.MAX_IMAGE_DIMENSION
    if max(img.width, img.height) > max_dim:
        ratio = max_dim / max(img.width, img.height)
        new_size = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
    return img


def apply_style_filter(image_path: str, style_type: str, output_path: str) -> None:
    """应用简单的风格滤镜（模拟模式）"""
    # 先做尺寸压缩
    img = resize_if_needed(image_path)

    if style_type == "anime":
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.5)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.2)
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.3)

    elif style_type == "oil_painting":
        img = img.filter(ImageFilter.SMOOTH_MORE)
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.4)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.15)

    elif style_type == "sketch":
        img = img.filter(ImageFilter.FIND_EDGES)
        img = img.point(lambda x: 255 - x)

    elif style_type == "watercolor":
        img = img.filter(ImageFilter.GaussianBlur(radius=2))
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(0.8)

    elif style_type == "pixel_art":
        small_size = (img.width // 8, img.height // 8)
        img = img.resize(small_size, Image.Resampling.NEAREST)
        img = img.resize((img.width * 8, img.height * 8), Image.Resampling.NEAREST)

    if output_path.lower().endswith((".jpg", ".jpeg")):
        img.save(output_path, "JPEG", quality=settings.JPEG_QUALITY, optimize=True)
    else:
        img.save(output_path, "PNG", optimize=True)


async def call_style_transfer(image_path: str, style_type: str) -> bytes:
    """调用风格转换（支持模拟模式和 Stability AI 真实 API）"""

    # 模拟模式（无需 API key）
    if settings.USE_MOCK_AI or not settings.STABILITY_API_KEY:
        output_path = os.path.join(
            settings.RESULT_DIR, f"result_{os.path.basename(image_path)}"
        )
        apply_style_filter(image_path, style_type, output_path)
        with open(output_path, "rb") as f:
            return f.read()

    # Stability AI 真实 API 模式
    # 先压缩图片再发送
    img = resize_if_needed(image_path)

    # 保存为临时 PNG 供上传
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        img.save(tmp.name, "PNG")
        tmp_path = tmp.name

    try:
        with open(tmp_path, "rb") as f:
            image_data = f.read()
    finally:
        os.unlink(tmp_path)

    prompt = STYLE_PROMPTS.get(style_type, STYLE_PROMPTS["anime"])

    async with httpx.AsyncClient(timeout=settings.AI_TIMEOUT_SECONDS) as client:
        resp = await client.post(
            settings.stability_api_base_url,
            headers={
                # Stability AI 使用小写 "authorization"
                "authorization": f"Bearer {settings.STABILITY_API_KEY}",
                "accept": "image/*",
            },
            files={"image": ("image.png", image_data, "image/png")},
            data={
                "prompt": prompt,
                # 图生图必填参数
                "mode": "image-to-image",
                "strength": settings.STYLE_STRENGTH,
                "output_format": "png",
            },
        )

        if resp.status_code != 200:
            raise RuntimeError(f"Stability AI 返回 {resp.status_code}: {resp.text[:500]}")

        return resp.content
