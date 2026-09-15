"""
Base43 API endpoints for Belentani Judas Experience
Provides access to the Base 43 Extension System
"""

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Dict, Optional

from app.services.base43 import Base43System, create_base43_instance
from app.config import get_settings

router = APIRouter(prefix="/api/base43")

# Global Base43 instance
base43_system = create_base43_instance(get_settings().frequency_hz)

@router.get("/info")
async def get_base43_info():
    """Get Base43 system information"""
    return {
        "system_name": "Base43 Extension System",
        "seed_frequency": base43_system.seed_frequency,
        "total_phases": len(base43_system.phases),
        "description": "Extends the 5-phase system to 43 phases with frequency operations"
    }

@router.get("/phases")
async def get_all_phases():
    """Get all 43 phases"""
    phases = []
    for phase in base43_system.phases:
        phases.append({
            "id": phase.id,
            "name": phase.name,
            "description": phase.description,
            "frequency": phase.frequency,
            "color": phase.color,
            "gem": phase.gem,
            "parent_phase": phase.parent_phase,
            "children": phase.children,
            "octave_equivalent": phase.octave_equivalent
        })
    return {"phases": phases}

@router.get("/phases/{phase_id}")
async def get_phase(phase_id: int):
    """Get specific phase by ID"""
    phase = base43_system.phase_map.get(phase_id)
    if not phase:
        raise HTTPException(status_code=404, detail="Phase not found")
    
    return {
        "id": phase.id,
        "name": phase.name,
        "description": phase.description,
        "frequency": phase.frequency,
        "color": phase.color,
        "gem": phase.gem,
        "parent_phase": phase.parent_phase,
        "children": phase.children,
        "octave_equivalent": phase.octave_equivalent,
        "intervals": base43_system.get_phase_intervals(phase.id)
    }

@router.get("/harmonic-chain")
async def get_harmonic_chain(
    start_phase: int = Query(..., description="Starting phase ID"),
    max_depth: int = Query(5, ge=1, le=10, description="Maximum chain depth")
):
    """Generate harmonic chain from starting phase"""
    if start_phase not in base43_system.phase_map:
        raise HTTPException(status_code=404, detail="Starting phase not found")
    
    chain = base43_system.get_harmonic_chain(start_phase, max_depth)
    
    return {
        "start_phase": start_phase,
        "chain": chain,
        "chain_depth": len(chain),
        "total_connections": sum(len(connections) for connections in chain)
    }

@router.get("/search")
async def search_phases(
    query: str = Query(..., description="Search query"),
    frequency: Optional[float] = Query(None, description="Search by frequency")
):
    """Search phases by name, gem, or frequency"""
    results = []
    
    if frequency:
        # Search by frequency
        phase = base43_system.get_phase_by_frequency(frequency)
        if phase:
            results.append({
                "id": phase.id,
                "name": phase.name,
                "description": phase.description,
                "frequency": phase.frequency,
                "color": phase.color,
                "gem": phase.gem,
                "match_type": "frequency"
            })
    else:
        # Search by query
        query_lower = query.lower()
        for phase in base43_system.phases:
            if (query_lower in phase.name.lower() or 
                query_lower in phase.description.lower() or 
                query_lower in phase.gem.lower()):
                results.append({
                    "id": phase.id,
                    "name": phase.name,
                    "description": phase.description,
                    "frequency": phase.frequency,
                    "color": phase.color,
                    "gem": phase.gem,
                    "match_type": "text"
                })
    
    return {
        "query": query if not frequency else f"frequency:{frequency}",
        "results": results,
        "total_results": len(results)
    }

@router.get("/intervals")
async def get_all_intervals(
    phase_id: Optional[int] = Query(None, description="Get intervals for specific phase")
):
    """Get phase intervals"""
    if phase_id is not None:
        if phase_id not in base43_system.phase_map:
            raise HTTPException(status_code=404, detail="Phase not found")
        intervals = base43_system.get_phase_intervals(phase_id)
        return {"phase_id": phase_id, "intervals": intervals}
    else:
        # Get all intervals
        all_intervals = {}
        for phase in base43_system.phases:
            all_intervals[phase.id] = base43_system.get_phase_intervals(phase.id)
        return {"all_intervals": all_intervals}

@router.post("/reset")
async def reset_base43_system():
    """Reset Base43 system with new seed frequency"""
    global base43_system
    base43_system = create_base43_instance(get_settings().frequency_hz)
    return {"message": "Base43 system reset", "seed_frequency": base43_system.seed_frequency}

@router.get("/statistics")
async def get_system_statistics():
    """Get Base43 system statistics"""
    frequencies = [phase.frequency for phase in base43_system.phases]
    
    return {
        "total_phases": len(base43_system.phases),
        "frequency_range": {
            "min": min(frequencies),
            "max": max(frequencies),
            "mean": sum(frequencies) / len(frequencies),
            "median": sorted(frequencies)[len(frequencies) // 2]
        },
        "gem_distribution": {
            gem: sum(1 for phase in base43_system.phases if phase.gem == gem)
            for gem in set(phase.gem for phase in base43_system.phases)
        },
        "parent_child_relationships": sum(1 for phase in base43_system.phases if phase.parent_phase is not None),
        "total_children": sum(len(phase.children) for phase in base43_system.phases),
        "harmonic_pairs": len([
            (phase1, phase2) 
            for phase1 in base43_system.phases 
            for phase2 in base43_system.phases 
            if phase1.id < phase2.id and phase1.is_harmonic(phase2)
        ])
    }

@router.get("/compatibility")
async def get_phase_compatibility(
    phase1_id: int = Query(..., description="First phase ID"),
    phase2_id: int = Query(..., description="Second phase ID")
):
    """Get compatibility analysis between two phases"""
    phase1 = base43_system.phase_map.get(phase1_id)
    phase2 = base43_system.phase_map.get(phase2_id)
    
    if not phase1 or not phase2:
        raise HTTPException(status_code=404, detail="One or both phases not found")
    
    interval = phase1.get_phase_interval(phase2)
    is_harmonic = phase1.is_harmonic(phase2)
    
    return {
        "phase1": {
            "id": phase1.id,
            "name": phase1.name,
            "frequency": phase1.frequency,
            "gem": phase1.gem
        },
        "phase2": {
            "id": phase2.id,
            "name": phase2.name,
            "frequency": phase2.frequency,
            "gem": phase2.gem
        },
        "analysis": {
            "interval_cents": interval,
            "interval_ratio": phase1.frequency / phase2.frequency,
            "is_harmonic": is_harmonic,
            "compatibility_score": 100 - abs(interval) if is_harmonic else max(0, 100 - abs(interval))
        }
    }

@router.get("/export")
async def export_base43_data(
    format: str = Query("json", regex="^(json|csv)$", description="Export format")
):
    """Export Base43 system data"""
    if format == "json":
        return JSONResponse(content={"phases": [
            {
                "id": phase.id,
                "name": phase.name,
                "description": phase.description,
                "frequency": phase.frequency,
                "color": phase.color,
                "gem": phase.gem,
                "parent_phase": phase.parent_phase,
                "children": phase.children,
                "octave_equivalent": phase.octave_equivalent
            } for phase in base43_system.phases
        ]})
    
    elif format == "csv":
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "Name", "Description", "Frequency", "Color", "Gem", "Parent Phase", "Children", "Octave Equivalent"])
        
        for phase in base43_system.phases:
            writer.writerow([
                phase.id,
                phase.name,
                phase.description,
                phase.frequency,
                phase.color,
                phase.gem,
                phase.parent_phase,
                ",".join(map(str, phase.children)),
                phase.octave_equivalent
            ])
        
        return JSONResponse(content={"csv": output.getvalue()}, media_type="text/csv")