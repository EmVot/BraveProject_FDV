from ast import Dict
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
from scipy.interpolate import interp1d
import cv2
import os
from typing import List, Tuple, Optional, Dict
from enum import Enum
from RusselSpacePartition import POLAR_REGIONS 


class TrailMode(Enum):
    """Modalità di visualizzazione della scia."""
    GROWING = "growing"  # Scia che cresce fino a mostrare tutta la traiettoria
    FIXED_LENGTH = "fixed_length"  # Scia di lunghezza fissa


class CircumplexPlotter:
    """
    A class to plot Russel's Circumplex Model of affects,
    with custom regions defined through polar coordinates.
    """
    
    def __init__(self, figsize=(10, 10)):
        """
        Initiatialize plotter.
        
        Args:
            figsize (tuple): Figure Dimensions (larghezza, altezza)
        """
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.regions = {}
        self._setup_base_figure()

    def _setup_detailed_grid(self):
        """
        Setup a detailed grid with:
        - Vertical and Horizontal lines with grid_step
        - Main bisectors
        """
        self.ax.grid(False)
        
        grid_step = 0.1
        grid_range = np.arange(-1.0, 1.1, grid_step)  
        
        for pos in grid_range:
            if abs(pos) < 1e-10: 
                continue
            
            self.ax.axvline(x=pos, color='gray', linewidth=0.5, alpha=0.6, linestyle='--')
            self.ax.axhline(y=pos, color='gray', linewidth=0.5, alpha=0.6, linestyle='--')
        
        self.ax.axhline(y=0, color='black', linewidth=2)
        self.ax.axvline(x=0, color='black', linewidth=2)
        
        self.ax.plot([-1, 1], [-1, 1], color='black', linewidth=2, alpha=0.8)
        
        self.ax.plot([-1, 1], [1, -1], color='black', linewidth=2, alpha=0.8)

        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
    
    def _setup_base_figure(self):
        """Setup base figure with unitary circle and axes"""
        self.ax.set_xlim(-1., 1.)
        self.ax.set_ylim(-1., 1.)
        self.ax.set_aspect('equal')
        
        self._setup_detailed_grid()
        
        circle = plt.Circle((0, 0), 1, fill=False, color='black', linewidth=2)
        self.ax.add_patch(circle)
        
        self.ax.text(0, 1.1, 'Aroused', ha='center', va='bottom', fontsize=12, fontweight='bold')
        self.ax.text(0, -1.1, 'Calm', ha='center', va='top', fontsize=12, fontweight='bold')
        self.ax.text(1.1, 0, 'Positive', ha='left', va='center', fontsize=12, fontweight='bold')
        self.ax.text(-1.1, 0, 'Negative', ha='right', va='center', fontsize=12, fontweight='bold')
        
        self.ax.set_title('Circumplex Model', fontsize=16, fontweight='bold', pad=60)
    
    def add_point(self, r, theta, label, point_color='black', point_size=50, 
                  label_color='gray', label_size=9, label_offset=0.05):
        """
        Add a point with the a label to the plot, using polar coordinates.
        
        Args:
            r (float): Radius (0 <= r <= 1)
            theta (float): Angle in Degrees 
            label (str): Label of the point
            point_color (str): Color of the point
            point_size (int): Size of the point
            label_color (str): Color of the label
            label_size (int): Font size of the label
            label_offset (float): Offset for label position from the point
        
        Returns:
            dict: information about the added point
        """
        # if not (0 <= r <= 1):
        #     raise ValueError("Radius must be: 0 <= r <= 1")
        
        theta_rad = np.radians(theta)
        x = r * np.cos(theta_rad)
        y = r * np.sin(theta_rad)
        
        self.ax.scatter(x, y, c=point_color, s=point_size, zorder=5, alpha=0.8)
        
        label_x = (r + label_offset) * np.cos(theta_rad)
        label_y = (r + label_offset) * np.sin(theta_rad)
        
        self.ax.text(label_x, label_y, label, 
                    fontsize=label_size, color=label_color,
                    ha='center', va='center'
                    )
        
        point_info = {
            'r': r,
            'theta': theta,
            'x': x,
            'y': y,
            'label': label,
            'point_color': point_color,
            'point_size': point_size,
            'label_color': label_color,
            'label_size': label_size
        }
        
        return point_info
    
    def add_region(self, r_inner, r_outer, theta_start, theta_end, color='blue', alpha=0.6, label=None):
        """
        Add a region (slice of circular crown) to the plot.
        
        Args:
            r_inner (float): Inner Radius (0 <= r_inner < r_outer <= 1)
            r_outer (float): Outer Radius (r_inner < r_outer <= 1)
            theta_start (float): Start Angle in degrees 
            theta_end (float): End Angle in degrees
            color (str): Color of the region
            alpha (float): Opacity of the region
            label (str): Label of the region
        """
        # if not (0 <= r_inner < r_outer <= 1):
        #     raise ValueError(f"It must be: 0 <= r_inner < r_outer <= 1, instead r_inner={r_inner}, r_outer={r_outer}")
        
        theta_start_rad = np.radians(theta_start)
        theta_end_rad = np.radians(theta_end)
        
        n_points = 50 
        theta_outer = np.linspace(theta_start_rad, theta_end_rad, n_points)
        x_outer = r_outer * np.cos(theta_outer)
        y_outer = r_outer * np.sin(theta_outer)
        
        theta_inner = np.linspace(theta_end_rad, theta_start_rad, n_points)
        x_inner = r_inner * np.cos(theta_inner)
        y_inner = r_inner * np.sin(theta_inner)
        
        x_points = np.concatenate([x_outer, x_inner])
        y_points = np.concatenate([y_outer, y_inner])
        
        polygon = patches.Polygon(list(zip(x_points, y_points)), 
                                closed=True, facecolor=color, alpha=alpha, 
                                edgecolor='black', linewidth=1)
        self.ax.add_patch(polygon)
        
        if label:
            theta_mid = (theta_start_rad + theta_end_rad) / 2
            r_mid = (r_inner + r_outer) / 2
            x_label = r_mid * np.cos(theta_mid)
            y_label = r_mid * np.sin(theta_mid)
            
            self.ax.text(x_label, y_label, label, ha='center', va='center', 
                        fontsize=10, fontweight='bold', 
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
        
        region_info = {
            'radius': {
                'min': r_inner,
                'max': r_outer
                },
            'angle': {
                'min': theta_start,
                'max': theta_end
                },
            'color': color,
        }
        self.regions[label] = region_info
        
        return region_info
    
    def show_or_save(self, action='show', filename=None, dpi=800):
        """
        Show or Save the resulting plot.
        
        Args:
            action (str): 'show' or 'save'
            filename (str): Filename for saving the plot, mandatory for 'save'
            dpi (int): resolution for saving the plot in DPI
        """
        if action == 'show':
            plt.tight_layout()
            plt.show()
        elif action == 'save':
            if filename is None:
                raise ValueError("Filename is mandatory for 'save' action")
            plt.tight_layout()
            self.fig.savefig(filename, dpi=dpi, bbox_inches='tight')
            print(f"Plot has been saved as: {filename}")
        else:
            raise ValueError("Action must be 'show' or 'save'")


class RusselPlotAnimator:
    def __init__(self, width: int = 1920, height: int = 1080, fps: int = 30, dpi: int = 100,
                 polar_regions: Optional[Dict] = None):
        """
        Inizializza l'animatore per il Russel Plot.
        
        Args:
            width: Larghezza del video in pixel
            height: Altezza del video in pixel  
            fps: Frame per secondo
            dpi: DPI per matplotlib
            polar_regions: Dizionario di regioni polari per il Russel Plot.
        """
        self.width = width
        self.height = height
        self.fps = fps
        self.dpi = dpi
        
        self.fig_width = width / dpi
        self.fig_height = height / dpi
        
        self.waypoints: List[Tuple[float, float]] = []
        if polar_regions is None:
            polar_regions = POLAR_REGIONS
        self.setup_russel_plot(figsize=(self.fig_width, self.fig_height), polar_regions=polar_regions)
        
    def setup_russel_plot(self, figsize: Tuple[float, float] = (10,10),
                          polar_regions: Optional[Dict] = None):
        """
        Configura il grafico base del Russel Plot.
        
        Args:
           figsize: Dimensioni della figura
            polar_regions: Dizionario di regioni polari
        """
        circumplex = CircumplexPlotter(figsize)
        if polar_regions:
            for region in polar_regions.keys():
                circumplex.add_region(polar_regions[region]['radius']['min'], polar_regions[region]['radius']['max'],
                                polar_regions[region]['angle']['min'], polar_regions[region]['angle']['max'],
                                color=polar_regions[region]['color'], alpha=0.6, label=region)
                #print(f"Added region: {region}")
        
        self.fig = circumplex.fig
        self.ax = circumplex.ax
        self.regions = circumplex.regions

        #circumplex.show_or_save(action='show')
        
    def add_waypoint(self, x: float, y: float):
        """Aggiunge un punto di controllo alla traiettoria."""
        self.waypoints.append((x, y))
        
    def add_waypoints(self, points: List[Tuple[float, float]]):
        """Aggiunge multipli punti di controllo."""
        self.waypoints.extend(points)
        
    def _interpolate_trajectory(self, duration_per_segment: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Interpola la traiettoria tra tutti i waypoints.
        
        Args:
            duration_per_segment: Durata in secondi per ogni segmento
            
        Returns:
            Tuple di array numpy (x_coords, y_coords) interpolati
        """
        if len(self.waypoints) < 2:
            raise ValueError("Servono almeno 2 waypoints per creare una traiettoria")
            
        total_segments = len(self.waypoints) - 1
        total_frames = int(total_segments * duration_per_segment * self.fps)
        
        t_waypoints = np.linspace(0, total_segments, len(self.waypoints))
        
        x_waypoints = np.array([wp[0] for wp in self.waypoints])
        y_waypoints = np.array([wp[1] for wp in self.waypoints])
        
        if len(self.waypoints) == 2:
            # Interpolazione lineare per 2 punti
            t_interp = np.linspace(0, 1, total_frames)
            x_interp = x_waypoints[0] + t_interp * (x_waypoints[1] - x_waypoints[0])
            y_interp = y_waypoints[0] + t_interp * (y_waypoints[1] - y_waypoints[0])
        else:
            # Interpolazione spline per più punti
            f_x = interp1d(t_waypoints, x_waypoints, kind='cubic')
            f_y = interp1d(t_waypoints, y_waypoints, kind='cubic')
            
            t_interp = np.linspace(0, total_segments, total_frames)
            x_interp = f_x(t_interp)
            y_interp = f_y(t_interp)
            
        return x_interp, y_interp
   
    def create_frame_based_video(self, duration_per_segment: float = 1.0,
                                trail_mode: TrailMode = TrailMode.FIXED_LENGTH,
                                trail_length: int = 50,
                                output_path: str = "russel_plot_video.mp4",
                                temp_dir: str = "temp_frames"
                                ) -> str:
        """
        Crea un video generando frame individuali e combinandoli con OpenCV.
        
        Args:
            duration_per_segment: Durata in secondi per ogni segmento
            trail_length: Lunghezza della scia
            output_path: Percorso del video finale
            temp_dir: Directory temporanea per i frame
            
        Returns:
            Percorso del video creato
        """
        
        os.makedirs(temp_dir, exist_ok=True)
        
        # Interpola la traiettoria
        x_coords, y_coords = self._interpolate_trajectory(duration_per_segment)
                
        # Genera frame
        for frame_idx in range(len(x_coords)): 
            self.ax.clear()
            self.setup_russel_plot(figsize=(self.fig_width, self.fig_height), polar_regions=self.regions)       
            current_x, current_y = x_coords[frame_idx], y_coords[frame_idx]
            
            # # Traiettoria completa (tratteggiata completa)
            # self.ax.plot(x_coords, y_coords, 'g--', alpha=0.3, linewidth=1, label='Full Trajectory')
            
            if trail_mode == TrailMode.GROWING:
                # Modalità 1: Scia crescente (tutta la traiettoria fino al punto corrente)
                #print(f"Trail mode: {trail_mode}")
                if frame_idx > 0:
                    trail_x = x_coords[:frame_idx+1]
                    trail_y = y_coords[:frame_idx+1]
                    self.ax.plot(trail_x, trail_y, 'r-', linewidth=2, label='Trail')
            
            elif trail_mode == TrailMode.FIXED_LENGTH:
                # Modalità 2: Scia di lunghezza fissa
                start_idx = max(0, frame_idx - trail_length)
                trail_x = x_coords[start_idx:frame_idx+1]
                trail_y = y_coords[start_idx:frame_idx+1]
                if len(trail_x) > 1:
                    self.ax.plot(trail_x, trail_y, 'r-', alpha=0.7, linewidth=2, label='Trail')
            
            
            # Punto corrente
            self.ax.plot(current_x, current_y, 'ro', markersize=10, label='Current Position')
            
            # wp_x = [wp[0] for wp in self.waypoints]
            # wp_y = [wp[1] for wp in self.waypoints]
            # self.ax.plot(wp_x, wp_y, 'ks', markersize=8, alpha=0.5, label='Waypoints')
                        
            # Salva frame
            frame_path = os.path.join(temp_dir, f"frame_{frame_idx:06d}.png")
            self.fig.savefig(frame_path, dpi=self.dpi, bbox_inches='tight', 
                           facecolor='white', edgecolor='none')
            
            if frame_idx % 30 == 0:  # Progress ogni secondo
                print(f"Frame {frame_idx}/{len(x_coords)} completato")
        
        print("Creando video...")
        
        # Crea video
        # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        # video_writer = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))
        
        # for frame_idx in range(len(x_coords)):
        #     frame_path = os.path.join(temp_dir, f"frame_{frame_idx:06d}.png")
        #     frame = cv2.imread(frame_path)
        #     if frame is not None:
        #         video_writer.write(frame)
        
        # video_writer.release()
        
        # # Pulisci cartella frames
        # for frame_idx in range(len(x_coords)):
        #     frame_path = os.path.join(temp_dir, f"frame_{frame_idx:06d}.png")
        #     if os.path.exists(frame_path):
        #         os.remove(frame_path)
        # os.rmdir(temp_dir)
        
        print(f"Video creato: {output_path}")
        return output_path