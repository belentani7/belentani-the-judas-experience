"""
Base 43 Extension System for Belentani Judas Experience
Extends the 5-phase system to 43 phases with frequency operations
"""

import math
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import hashlib


@dataclass
class Phase:
    """Base 43 Phase with frequency operations"""
    id: int
    name: str
    description: str
    frequency: float  # Hz
    color: str
    gem: str
    parent_phase: Optional[int] = None
    children: List[int] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []
    
    @property
    def octave_equivalent(self) -> float:
        """Find equivalent frequency within octave 0-432Hz"""
        while self.frequency > 432:
            self.frequency /= 2
        return self.frequency
    
    def get_phase_interval(self, other_phase: 'Phase') -> float:
        """Calculate phase interval in cents (100th of a semitone)"""
        return 1200 * math.log2(self.frequency / other_phase.frequency)
    
    def is_harmonic(self, other_phase: 'Phase', tolerance: float = 5.0) -> bool:
        """Check if two phases are harmonic (within tolerance cents)"""
        interval = abs(self.get_phase_interval(other_phase))
        return interval < tolerance


class Base43System:
    """Base 43 Extension System"""
    
    def __init__(self, seed_frequency: float = 432.0):
        self.seed_frequency = seed_frequency
        self.phases: List[Phase] = []
        self.phase_map: Dict[int, Phase] = {}
        self.gem_colors: Dict[str, str] = {
            # Original 5 gems
            'void': '#050203',
            'blood': '#8a0d18', 
            'neon': '#ff1a3c',
            'crystal': 'rgba(255, 255, 255, 0.08)',
            'gold_key': '#c9a84c',
            # Extended 38 gems (pseudo-generative colors)
            'diamond': '#e8f4f8',
            'ruby': '#e74c3c',
            'sapphire': '#3498db',
            'emerald': '#27ae60',
            'amethyst': '#9b59b6',
            'pearl': '#f8f9fa',
            'onyx': '#2c3e50',
            'jade': '#00a86b',
            'topaz': '#f39c12',
            'aquamarine': '#40e0d0',
            'garnet': '#b91c3c',
            'zircon': '#ffc0cb',
            'moonstone': '#f8f8ff',
            'sunstone': '#ffa500',
            'opal': '#8b7355',
            'malachite': '#0f9d58',
            'lapis': '#26619c',
            'turquoise': '#40e0d0',
            'amber': '#ffbf00',
            'coral': '#ff7f50',
            'jadeite': '#00a86b',
            'spinel': '#ff4136',
            'alexandrite': '#4b0082',
            'morganite': '#ff69b4',
            'tanzanite': '#4b0082',
            'tsavorite': '#00a86b',
            'demantoid': '#50c878',
            'paraiba': '#40e0d0',
            'ruby_red': '#e74c3c',
            'blue_sapphire': '#1e3a8a',
            'yellow_sapphire': '#ffd700',
            'green_emerald': '#50c878',
            'purple_amethyst': '#9b59b6',
            'diamond_white': '#f8f8ff',
            'black_onyx': '#1c1c1c'
        }
        self._initialize_phases()
    
    def _initialize_phases(self) -> None:
        """Initialize the 43 phases from the base 5"""
        self.phases = []
        self.phase_map = {}
        
        # Base 5 phases (original)
        base_phases = [
            (0, 'void', 'Null phase', self.seed_frequency * 0.5, '#050203', 'void'),
            (1, 'blood', 'Life cycle', self.seed_frequency * 0.75, '#8a0d18', 'blood'),
            (2, 'neon', 'Electric potential', self.seed_frequency * 1.0, '#ff1a3c', 'neon'),
            (3, 'crystal', 'Pure resonance', self.seed_frequency * 1.5, 'rgba(255, 255, 255, 0.08)', 'crystal'),
            (4, 'gold_key', 'Transcendence', self.seed_frequency * 2.0, '#c9a84c', 'gold_key'),
        ]
        
        # Create base phases
        for i, name, desc, freq, color, gem in base_phases:
            phase = Phase(i, name, desc, freq, color, gem)
            self.phases.append(phase)
            self.phase_map[i] = phase
        
        # Generate extended 38 phases using mathematical relationships
        self._generate_extended_phases()
    
    def _generate_extended_phases(self) -> None:
        """Generate 38 additional phases using mathematical relationships"""
        # Generate patterns using prime numbers and golden ratio
        prime_numbers = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167]
        
        gem_names = list(self.gem_colors.keys())[5:]  # Exclude the original 5 gems
        
        for i in range(5, 43):
            # Calculate phase relationships
            phase_number = i
            parent_phase = (phase_number - 1) // 4  # Hierarchical structure
            
            # Generate frequency using prime number sequences and seed frequency
            if phase_number - 5 < len(prime_numbers):
                prime_factor = prime_numbers[phase_number - 5]
                frequency = self.seed_frequency * (prime_factor / 43.0)
            else:
                # Use golden ratio for additional phases
                golden_ratio = (1 + math.sqrt(5)) / 2
                frequency = self.seed_frequency * (golden_ratio ** ((phase_number - 40) / 10))
            
            # Normalize frequency to reasonable range
            while frequency > 1000:  # Keep frequencies reasonable
                frequency /= 2
            while frequency < 20:   # Avoid infrasound
                frequency *= 2
            
            # Get gem and color
            gem_index = (phase_number - 5) % len(gem_names)
            gem = gem_names[gem_index]
            color = self.gem_colors[gem]
            
            # Generate descriptive name based on phase characteristics
            name = self._generate_phase_name(phase_number, frequency)
            description = self._generate_phase_description(phase_number, frequency)
            
            phase = Phase(
                id=phase_number,
                name=name,
                description=description,
                frequency=frequency,
                color=color,
                gem=gem,
                parent_phase=parent_phase if parent_phase in self.phase_map else None
            )
            
            # Add children relationship to parent
            if parent_phase is not None and parent_phase in self.phase_map:
                self.phase_map[parent_phase].children.append(phase_number)
            
            self.phases.append(phase)
            self.phase_map[phase_number] = phase
    
    def _generate_phase_name(self, phase_number: int, frequency: float) -> str:
        """Generate descriptive name for phase"""
        base_names = [
            'void', 'blood', 'neon', 'crystal', 'gold_key',
            'diamond', 'ruby', 'sapphire', 'emerald', 'amethyst',
            'pearl', 'onyx', 'jade', 'topaz', 'aquamarine',
            'garnet', 'zircon', 'moonstone', 'sunstone', 'opal',
            'malachite', 'lapis', 'turquoise', 'amber', 'coral',
            'jadeite', 'spinel', 'alexandrite', 'morganite', 'tanzanite',
            'demantoid', 'paraiba', 'ruby_red', 'blue_sapphire', 'yellow_sapphire',
            'green_emerald', 'purple_amethyst', 'diamond_white', 'black_onyx'
        ]
        
        if phase_number - 5 < len(base_names):
            gem_name = base_names[phase_number - 5]
            
            # Add frequency-based modifiers
            if frequency < 100:
                return f"subsonic_{gem_name}"
            elif frequency < 200:
                return f"infra_{gem_name}"
            elif frequency < 300:
                return f"low_{gem_name}"
            elif frequency < 400:
                return f"mid_{gem_name}"
            elif frequency < 500:
                return f"high_{gem_name}"
            else:
                return f"ultra_{gem_name}"
        else:
            return f"phase_{phase_number}"
    
    def _generate_phase_description(self, phase_number: int, frequency: float) -> str:
        """Generate description for phase based on frequency and relationships"""
        desc_parts = []
        
        # Frequency-based characteristics
        if frequency < 50:
            desc_parts.append("Infrasonic resonance")
        elif frequency < 100:
            desc_parts.append("Subsonic vibration")
        elif frequency < 200:
            desc_parts.append("Low frequency wave")
        elif frequency < 300:
            desc_parts.append("Mid frequency oscillation")
        elif frequency < 400:
            desc_parts.append("High frequency pulse")
        else:
            desc_parts.append("Ultrasonic energy")
        
        # Phase relationships
        if phase_number > 4:
            parent = self.phase_map.get((phase_number - 1) // 4)
            if parent:
                interval = abs(frequency - parent.frequency)
                if interval < 50:
                    desc_parts.append(f"Child of {parent.name}")
                else:
                    desc_parts.append(f"Harmonic to {parent.name}")
        
        # Gem properties
        gem = self.gem_colors.get(list(self.gem_colors.keys())[phase_number % len(self.gem_colors)], 'unknown')
        desc_parts.append(f"Gem resonance: {gem}")
        
        return "; ".join(desc_parts)
    
    def get_phase_by_frequency(self, target_frequency: float, tolerance: float = 5.0) -> Optional[Phase]:
        """Find phase closest to target frequency"""
        best_phase = None
        best_difference = float('inf')
        
        for phase in self.phases:
            difference = abs(phase.frequency - target_frequency)
            if difference < best_difference:
                best_difference = difference
                best_phase = phase
        
        if best_difference <= tolerance:
            return best_phase
        return None
    
    def get_harmonic_chain(self, start_phase: int, max_depth: int = 5) -> List[List[int]]:
        """Generate harmonic chain from starting phase"""
        chain = []
        current_phases = [start_phase]
        
        for depth in range(max_depth):
            next_phases = []
            harmonic_intervals = []
            
            for phase_id in current_phases:
                current_phase = self.phase_map.get(phase_id)
                if not current_phase:
                    continue
                
                harmonics = []
                for other_phase in self.phases:
                    if other_phase.id != phase_id and current_phase.is_harmonic(other_phase):
                        harmonics.append(other_phase.id)
                
                next_phases.extend(harmonics)
                harmonic_intervals.append(harmonics)
            
            chain.append(harmonic_intervals)
            current_phases = next_phases
        
        return chain
    
    def get_phase_intervals(self, phase_id: int) -> Dict[str, float]:
        """Get intervals from phase to all other phases in cents"""
        intervals = {}
        phase = self.phase_map.get(phase_id)
        
        if not phase:
            return intervals
        
        for other_phase in self.phases:
            if other_phase.id != phase_id:
                interval = phase.get_phase_interval(other_phase)
                intervals[f"phase_{other_phase.id}"] = interval
        
        return intervals
    
    def save_phase_data(self, file_path: Path) -> None:
        """Save phase data to JSON file"""
        phase_data = []
        
        for phase in self.phases:
            phase_data.append({
                'id': phase.id,
                'name': phase.name,
                'description': phase.description,
                'frequency': phase.frequency,
                'color': phase.color,
                'gem': phase.gem,
                'parent_phase': phase.parent_phase,
                'children': phase.children,
                'octave_equivalent': phase.octave_equivalent
            })
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(phase_data, f, indent=2, ensure_ascii=False)
    
    def load_phase_data(self, file_path: Path) -> None:
        """Load phase data from JSON file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            phase_data = json.load(f)
        
        self.phases = []
        self.phase_map = {}
        
        for phase_info in phase_data:
            phase = Phase(**phase_info)
            self.phases.append(phase)
            self.phase_map[phase.id] = phase


def create_base43_instance(seed_frequency: float = 432.0) -> Base43System:
    """Factory function to create Base43 system instance"""
    return Base43System(seed_frequency)