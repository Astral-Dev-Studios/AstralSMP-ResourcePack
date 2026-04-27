#version 150

#moj_import <fog.glsl>

uniform sampler2D Sampler0;

uniform vec4 ColorModulator;
uniform float FogStart;
uniform float FogEnd;
uniform vec4 FogColor;

in float vertexDistance;
in vec4 vertexColor;
in vec2 texCoord0;
in vec2 texCoord1;
in vec4 normal;

out vec4 fragColor;

void main() {
    vec4 color = texture(Sampler0, texCoord0) * vertexColor * ColorModulator;

    ivec2 texSize = textureSize(Sampler0, 0);
    
    if (texSize.x == 64 && texSize.y == 64) {
        vec2 uv = texCoord0 * 64.0;
        
        bool isRightArmL1 = uv.x >= 40.0 && uv.x <= 56.0 && uv.y >= 16.0 && uv.y <= 32.0;
        bool isRightArmL2 = uv.x >= 40.0 && uv.x <= 56.0 && uv.y >= 32.0 && uv.y <= 48.0;
        
        bool isLeftArmL1 = uv.x >= 32.0 && uv.x <= 48.0 && uv.y >= 48.0 && uv.y <= 64.0;
        bool isLeftArmL2 = uv.x >= 48.0 && uv.x <= 64.0 && uv.y >= 48.0 && uv.y <= 64.0;
        
        bool isRightLegL1 = uv.x >= 0.0 && uv.x <= 16.0 && uv.y >= 16.0 && uv.y <= 32.0;
        bool isRightLegL2 = uv.x >= 0.0 && uv.x <= 16.0 && uv.y >= 32.0 && uv.y <= 48.0;
        
        bool isLeftLegL1 = uv.x >= 16.0 && uv.x <= 32.0 && uv.y >= 48.0 && uv.y <= 64.0;
        bool isLeftLegL2 = uv.x >= 0.0 && uv.x <= 16.0 && uv.y >= 48.0 && uv.y <= 64.0;
        
        bool isArm = isRightArmL1 || isRightArmL2 || isLeftArmL1 || isLeftArmL2;
        bool isLeg = isRightLegL1 || isRightLegL2 || isLeftLegL1 || isLeftLegL2;
        
        if (isArm || isLeg) {
            discard;
        }
    }

    if (color.a < 0.1) {
        discard;
    }
    
    fragColor = linear_fog(color, vertexDistance, FogStart, FogEnd, FogColor);
}