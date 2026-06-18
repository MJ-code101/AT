from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn

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
        
        response = {
            "status": "success",
            "message": f"Scene {scene.scene_id} analyzed successfully",
            "scene_id": scene.scene_id,
            "object_count": len(scene.objects),
            "room_count": len(scene.rooms),
            "scores": scene.scores,
            "issues": scene.issues,
            "user_action": {
                "action": scene.user_action.action,
                "target": scene.user_action.target_id
            },
            "analysis": {
                "total_objects": len(scene.objects),
                "object_types": list(set(obj.type for obj in scene.objects)),
                "rooms_detected": [room.room_type for room in scene.rooms]
            }
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Scene Analysis API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)