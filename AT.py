from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import json

app = FastAPI()

class Position(BaseModel):
    x: float
    y: float
    z: float

class Rotation(BaseModel):
    x: float
    y: float
    z: float

class Scale(BaseModel):
    x: float
    y: float
    z: float

class Dimensions(BaseModel):
    width: float
    height: float
    depth: float

class Relationships(BaseModel):
    attached_to: Optional[str] = None
    faces: Optional[str] = None
    near: List[str] = []

class Clearance(BaseModel):
    front: float
    back: float
    left: float
    right: float

class State(BaseModel):
    selected: bool
    movable: bool
    resizable: bool

class Object(BaseModel):
    id: str
    type: str
    category: str
    position: Position
    rotation: Rotation
    scale: Scale
    dimensions: Dimensions
    style: List[str]
    material: List[str]
    color: List[str]
    tags: List[str]
    relationships: Relationships
    clearance: Clearance
    state: State

class Room(BaseModel):
    room_id: str
    room_type: str
    style: List[str]
    objects: List[str]

class UserAction(BaseModel):
    action: str
    target_id: str

class SceneData(BaseModel):
    scene_id: str
    user_action: UserAction
    rooms: List[Room]
    objects: List[Object]
    scores: Dict[str, float]
    issues: List[str]

class SceneRequest(BaseModel):
    scene_data: SceneData

@app.post("/analyze_scene")
async def analyze_scene(request: SceneRequest):
    try:
        scene = request.scene_data
        
        # Dummy response payload
        dummy_response = {
            "status": "success",
            "message": f"Scene {scene.scene_id} analyzed successfully",
            "scene_id": scene.scene_id,
            "object_count": len(scene.objects),
            "room_count": len(scene.rooms),
            "scores": {
                "spacing": 0.85,
                "walkability": 0.92,
                "style_consistency": 0.88,
                "lighting": 0.75,
                "functionality": 0.90
            },
            "issues": [
                "tv_distance_too_close",
                "sofa_obstructing_pathway",
                "low_lighting_in_corners"
            ],
            "user_action": {
                "action": scene.user_action.action,
                "target": scene.user_action.target_id,
                "status": "completed"
            },
            "analysis": {
                "total_objects": len(scene.objects),
                "object_types": list(set(obj.type for obj in scene.objects)),
                "rooms_detected": [room.room_type for room in scene.rooms],
                "recommendations": [
                    "Move sofa 0.5m away from TV",
                    "Add floor lamp in corner",
                    "Create clear pathway to exit"
                ],
                "quality_score": 4.2,
                "max_capacity": 6,
                "optimization_possible": True
            },
            "timestamp": "2026-06-18T10:30:00Z",
            "version": "2.1.0"
        }
        
        return dummy_response
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Scene Analysis API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)