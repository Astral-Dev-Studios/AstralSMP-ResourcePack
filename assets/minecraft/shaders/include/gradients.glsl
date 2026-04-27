#version 150

const float tolerance = 2.5;

bool isColor(vec3 inputRGB, vec3 targetRGB) {
    return abs(inputRGB.r - targetRGB.r) < tolerance &&
           abs(inputRGB.g - targetRGB.g) < tolerance &&
           abs(inputRGB.b - targetRGB.b) < tolerance;
}

// Main logic function
vec4 applyGradient(vec4 originalColor, vec2 uv) {
    vec3 inputRGB = originalColor.rgb * 255.0;
    float fade = uv.y;

    if (isColor(inputRGB, vec3(63.0, 81.0, 44.0))) {
        vec3 top = vec3(34.0, 193.0, 195.0) / 255.0;
        vec3 bot = vec3(253.0, 187.0, 45.0) / 255.0;
        return vec4(mix(top, bot, fade), originalColor.a);
    }

    return originalColor;
}