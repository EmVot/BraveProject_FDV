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
from RusselSpacePartition import POLAR_REGIONS, AREA_LABELS 


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
                  label_color='gray', label_size=9, label_offset=0.05, is_polar=True):
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
        if is_polar:
            theta_rad = np.radians(theta)
            x = r * np.cos(theta_rad)
            y = r * np.sin(theta_rad)
        else:
            x = r
            y = theta
        
        self.ax.scatter(x, y, c=point_color, s=point_size, zorder=5)
        
        label_x = (x + label_offset) 
        label_y = (y + label_offset)
        
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
    
    def add_region(self, r_inner, r_outer, theta_start, theta_end, color='blue', alpha=0.8, label=None, include_label=False):
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
        
        if color == '#ffd166':
            polygon = patches.Polygon(list(zip(x_points, y_points)), 
                                closed=True, fill=False,
                                edgecolor='black', linewidth=1)
        else:
            polygon = patches.Polygon(list(zip(x_points, y_points)), 
                                closed=True, facecolor=color, alpha=alpha, 
                                edgecolor='black', linewidth=1)
        self.ax.add_patch(polygon)
        
        if label and include_label:
            theta_mid = (theta_start_rad + theta_end_rad) / 2
            r_mid = (r_inner + r_outer) / 2
            x_label = r_mid * np.cos(theta_mid)
            y_label = r_mid * np.sin(theta_mid)
            
            self.ax.text(x_label, y_label, label, ha='center', va='center', 
                        fontsize=7, fontweight='bold', 
                        bbox=dict(boxstyle='round,pad=0.1', facecolor='white', alpha=0.8))
        
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
                 polar_regions: Optional[Dict] = None, area_labels: bool = True):
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
        
        self.waypoints = []
        if polar_regions is None:
            polar_regions = POLAR_REGIONS
        if area_labels:
            self.setup_russel_plot(figsize=(self.fig_width, self.fig_height), polar_regions=polar_regions, area_labels=AREA_LABELS)
        else:
            self.setup_russel_plot(figsize=(self.fig_width, self.fig_height), polar_regions=polar_regions)
        
    def setup_russel_plot(self, figsize: Tuple[float, float] = (10,10),
                          polar_regions: Optional[Dict] = None, area_labels: Optional[Dict] = None):
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
        axis_threshold = 0.1
        ocra_color = '#CC8800'
        if area_labels:
            for i, (label, (x,y)) in enumerate(area_labels.items()):
                is_near_x_axis = abs(y) < axis_threshold
                is_near_y_axis = abs(x) < axis_threshold
                is_near_axes = is_near_x_axis or is_near_y_axis
                if is_near_axes:
                    # Label normale (orizzontale) per punti prossimi agli assi
                    rotation = 0
                    if i == 4: 
                        ha = 'left'
                        va = 'bottom'
                    elif i == 9:
                        ha = 'center'
                        va = 'top'
                    elif i == 14:
                        ha = 'right'
                        va = 'bottom'
                    elif i == 19:
                        ha = 'center'
                        va = 'bottom'
                else:
                    # Label obliqua seguendo la retta che passa per l'origine
                    angle_rad = np.arctan2(y, x)
                    rotation = np.degrees(angle_rad)

                    # Regola l'orientamento del testo per evitare che sia capovolto
                    if rotation > 90:
                        rotation -= 180
                    elif rotation < -90:
                        rotation += 180
                    if i < 5: 
                        ha = 'left'
                        va = 'bottom'
                    if i >=5 and i<10 : 
                        ha = 'left'
                        va = 'top'
                    if i >=10 and i<15 :
                        ha = 'right'
                        va = 'top'
                    if i >=15 and i<20 :
                        ha = 'right'
                        va = 'bottom'
                    
                # Aggiungi la label al grafico
                circumplex.ax.text(x, y, label, 
                         rotation=rotation,
                         horizontalalignment=ha,
                         verticalalignment=va,
                         color=ocra_color,
                         fontsize=10,  
                         bbox=None)

        self.fig = circumplex.fig
        self.ax = circumplex.ax
        self.regions = circumplex.regions

        #circumplex.show_or_save(action='show')
        
    def add_waypoints(self, points):
        """Aggiunge multipli punti di controllo."""
        self.waypoints.extend(points)
        
    # def _interpolate_trajectory(self, duration_per_segment: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
    #     """
    #     Interpola la traiettoria tra tutti i waypoints.
        
    #     Args:
    #         duration_per_segment: Durata in secondi per ogni segmento
            
    #     Returns:
    #         Tuple di array numpy (x_coords, y_coords) interpolati
    #     """
    #     if len(self.waypoints) < 2:
    #         raise ValueError("Servono almeno 2 waypoints per creare una traiettoria")
            
    #     total_segments = len(self.waypoints) - 1
    #     total_frames = int(total_segments * duration_per_segment * self.fps)
        
    #     t_waypoints = np.linspace(0, total_segments, len(self.waypoints))
        
    #     x_waypoints = np.array([wp['position'][0] for wp in self.waypoints])
    #     y_waypoints = np.array([wp['position'][1] for wp in self.waypoints])
        
    #     if len(self.waypoints) == 2:
    #         # Interpolazione lineare per 2 punti
    #         t_interp = np.linspace(0, 1, total_frames)
    #         x_interp = x_waypoints[0] + t_interp * (x_waypoints[1] - x_waypoints[0])
    #         y_interp = y_waypoints[0] + t_interp * (y_waypoints[1] - y_waypoints[0])
    #     else:
    #         # Interpolazione spline per più punti
    #         f_x = interp1d(t_waypoints, x_waypoints, kind='cubic')
    #         f_y = interp1d(t_waypoints, y_waypoints, kind='cubic')
            
    #         t_interp = np.linspace(0, total_segments, total_frames)
    #         x_interp = f_x(t_interp)
    #         y_interp = f_y(t_interp)
            
    #     return x_interp, y_interp

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
            
        # Calcola il numero di frame per segmento
        frames_per_segment = int(duration_per_segment * self.fps)
        
        # Array per raccogliere tutti i punti interpolati
        x_coords = []
        y_coords = []
        
        # Interpola ogni segmento separatamente
        for i in range(len(self.waypoints)-1):
            start_wp = self.waypoints[i]['position']
            end_wp = self.waypoints[i + 1]['position']
            
            # Per l'ultimo segmento, includi anche il punto finale
            # Per gli altri segmenti, escludi il punto finale per evitare duplicati
            if i == len(self.waypoints) - 2:  # ultimo segmento
                t_segment = np.linspace(0, 1, frames_per_segment + 1)
                include_end = True
            else:
                t_segment = np.linspace(0, 1, frames_per_segment + 1)[:-1]  # escludi ultimo punto
                include_end = False
            
            # Interpolazione lineare semplice per ogni segmento
            x_segment = start_wp[0] + t_segment * (end_wp[0] - start_wp[0])
            y_segment = start_wp[1] + t_segment * (end_wp[1] - start_wp[1])

            x_coords.extend([start_wp[0] for _ in range(14)])
            y_coords.extend([start_wp[1] for _ in range(14)])

            x_coords.extend(x_segment)
            y_coords.extend(y_segment)
            # Aggiungi il punto finale se necessario
            if include_end:
                x_coords.extend([end_wp[0] for _ in range(15)])
                y_coords.extend([end_wp[1] for _ in range(15)])
        print(f"Interpolated {len(x_coords)} points in total")
       
        return x_coords, y_coords
   
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
        label_offset = 0.08
        # Interpola la traiettoria
        x_coords, y_coords = self._interpolate_trajectory(duration_per_segment)
        x_waypoints = [wp['position'][0] for wp in self.waypoints]
        y_waypoints = [wp['position'][1] for wp in self.waypoints]
        idx = 0
        
     
        # Genera frame
        for frame_idx in range(len(x_coords)): 
            
            self.ax.clear()
            self.setup_russel_plot(figsize=(self.fig_width, self.fig_height), polar_regions=self.regions, area_labels=AREA_LABELS)       
            current_x, current_y = x_coords[frame_idx], y_coords[frame_idx]
            
            # # Traiettoria completa (tratteggiata completa)
            # self.ax.plot(x_coords, y_coords, 'g--', alpha=0.3, linewidth=1, label='Full Trajectory')
            
            if trail_mode == TrailMode.GROWING:
                # Modalità 1: Scia crescente (tutta la traiettoria fino al punto corrente)
                #print(f"Trail mode: {trail_mode}")
                if frame_idx > 0:
                    trail_x = x_coords[:frame_idx+1]
                    trail_y = y_coords[:frame_idx+1]
                    self.ax.plot(trail_x, trail_y, '#ba0be0', linewidth=4, label='Trail')
            
            elif trail_mode == TrailMode.FIXED_LENGTH:
                # Modalità 2: Scia di lunghezza fissa
                start_idx = max(0, frame_idx - trail_length)
                trail_x = x_coords[start_idx:frame_idx+1]
                trail_y = y_coords[start_idx:frame_idx+1]
                if len(trail_x) > 1:
                    self.ax.plot(trail_x, trail_y, 'r-', alpha=0.7, linewidth=2, label='Trail')
            
            
            # Punto corrente
            if current_x == x_waypoints[idx//15] and current_y == y_waypoints[idx//15]:
                
                self.ax.scatter(current_x, current_y, color=self.waypoints[idx//15]['color'],
                              s=60, edgecolors='black', zorder=5)
                self.ax.text(current_x+label_offset, current_y+label_offset, self.waypoints[idx//15]['label'], 
                    fontsize=18, color='black', weight='bold',
                    ha='center', va='center'
                    )
                idx += 1
                
                
            else:
                self.ax.plot(current_x, current_y, 'gray', markersize=10, label='Current Position')
            
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
    
        # Create video 
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
        video_writer = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))

        # Check if VideoWriter was initialized properly
        if not video_writer.isOpened():
            print(f"Failed to open video writer with mp4v codec. Trying alternative codecs...")
            video_writer.release()
            
            # Try alternative codecs
            for codec in ['XVID', 'X264', 'avc1']:
                fourcc = cv2.VideoWriter_fourcc(*codec)
                video_writer = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))
                if video_writer.isOpened():
                    print(f"Successfully opened video writer with {codec} codec")
                    break
                video_writer.release()
            
            # If all codecs fail, try changing the file extension
            if not video_writer.isOpened():
                output_path_avi = output_path.replace('.mp4', '.avi')
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                video_writer = cv2.VideoWriter(output_path_avi, fourcc, self.fps, (self.width, self.height))
                if video_writer.isOpened():
                    print(f"Fallback: saving as AVI format to {output_path_avi}")
                    output_path = output_path_avi

        if not video_writer.isOpened():
            raise RuntimeError("Failed to initialize video writer with any codec")

        frames_written = 0
        for frame_idx in range(len(x_coords)):
            frame_path = os.path.join(temp_dir, f"frame_{frame_idx:06d}.png")
            
            if not os.path.exists(frame_path):
                print(f"Warning: Frame {frame_path} does not exist, skipping...")
                continue
                
            frame = cv2.imread(frame_path)
            if frame is None:
                print(f"Warning: Could not read frame {frame_path}, skipping...")
                continue
            
            # Ensure frame has the correct dimensions
            if frame.shape[:2] != (self.height, self.width):
                print(f"Warning: Frame {frame_idx} has dimensions {frame.shape[:2]}, expected ({self.height}, {self.width})")
                frame = cv2.resize(frame, (self.width, self.height))
            
            # Write frame
            success = video_writer.write(frame)
            if success:
                frames_written += 1
            else:
                print(f"Warning: Failed to write frame {frame_idx}")

        print(f"Successfully wrote {frames_written} frames to video")
        video_writer.release()

        # Verify the output file
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"Output video file size: {file_size} bytes")
            if file_size < 1000: 
                print("Warning: Output file is very small, possibly corrupted")
        else:
            print("Error: Output file was not created")
        # # Pulisci cartella frames
        # for frame_idx in range(len(x_coords)):
        #     frame_path = os.path.join(temp_dir, f"frame_{frame_idx:06d}.png")
        #     if os.path.exists(frame_path):
        #         os.remove(frame_path)
        # os.rmdir(temp_dir)
        
        print(f"Video creato: {output_path}")
        return output_path