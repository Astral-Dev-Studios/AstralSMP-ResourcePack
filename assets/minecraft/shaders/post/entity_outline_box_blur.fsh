#version 150

uniform sampler2D InSampler;   
uniform sampler2D MaskSampler; 
uniform sampler2D DiffuseDepthSampler;
uniform float GameTime;

in vec2 texCoord;
in vec2 sampleStep;

out vec4 fragColor;

float onOff(float a, float b, float c, float framecount) {
    return step(c, sin((framecount * 0.001) + a * cos((framecount * 0.001) * b)));
}

vec2 jumpy(vec2 uv, float framecount) {
    vec2 look = uv;
    float window = 1.0 / (1.0 + 80.0 * (look.y - mod(framecount / 4.0, 1.0)) * (look.y - mod(framecount / 4.0, 1.0)));
    look.x += 0.03 * sin(look.y * 10.0 + framecount) / 20.0 * onOff(4.0, 4.0, 0.3, framecount) * (0.5 + cos(framecount * 20.0)) * window;
    return look;
}

void main() {
    float t = GameTime * 1000.0;
    
    float bodyMask = texture(MaskSampler, texCoord).a;

    vec4 blurred = vec4(0.0);
    float radius = 1;
    for (float a = -radius; a <= radius; a += 3.0) {
        blurred += texture(InSampler, texCoord + sampleStep * a);
    }
    float outlineAlpha = clamp(blurred.a, 0.0, 1.0);

    vec2 vhsUV = jumpy(texCoord, mod(t, 7.0));
    float scanline = (mod(gl_FragCoord.y, 4.0) < 2.0) ? 0.12 : 0.0;
    float noise = fract(sin(dot(vhsUV + t, vec2(12.9898, 78.233))) * 43758.5453) * 0.05;

    if (outlineAlpha > 0.1 && bodyMask < 0.8) {
        fragColor = vec4(1.0, 1.0, 1.0, 1.0);
    } 
    else if (bodyMask > 0.1) {
        float gray = 0.4 + scanline + noise; 
        fragColor = vec4(vec3(gray), 0.3);
    } 
    else {
        discard;
    }
}