from PySide6.QtWidgets import (
    QWidget, 
    QGraphicsOpacityEffect,
    QLabel,
    QProgressBar
)
from PySide6.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve
)
from win_tb import WinTB

class prog:
    def __init__(self, main_obj):
        self.tb = WinTB(main_obj.winId())    

        WinTB.set_state(self.tb, "normal")
        prog.config_status_prog(main_obj, 'construct') #create progress elements in status bar 

    def update_val(self, main_obj, msg, value):
        WinTB.set_val(self.tb, value)         
        main_obj.ui.progress.setValue(value)
        main_obj.ui.status_label.setText(msg)  

    def indeterminate(self, main_obj, msg):
        WinTB.set_state(self.tb, "indeterminate")         
        main_obj.ui.status_label.setText(msg)  

    def close(self, main_obj):
        WinTB.set_state(self.tb, "normal")          
        prog.config_status_prog(main_obj, 'destruct') #remove progress elements in status bar

    def config_status_prog(main_obj, action: str):
        #configures status bar to show progress bar and message

        if action == 'construct':
            # Check for and cancel any running messages first
            if hasattr(main_obj, "_fade_anim"):
                main_obj._fade_anim.stop()
                msg.clear_fading_components(main_obj)

            # Create progress bar, add it to the status bar
            main_obj.ui.progress = QProgressBar()
            main_obj.ui.progress.setMaximumWidth(75)  
            main_obj.ui.progress.setAlignment(Qt.AlignCenter)    
            main_obj.ui.progress.setRange(0, 100)         
            main_obj.ui.statusbar.addWidget(main_obj.ui.progress)  

            # Create a permanent label inside the status bar (invisible at first)
            main_obj.ui.status_label = QLabel("")
            main_obj.ui.status_label.setMinimumWidth(400)   
            main_obj.ui.statusbar.addWidget(main_obj.ui.status_label)                   

            #extra spacer to push prior items to left
            main_obj.ui.status_spacer = QWidget()    
            main_obj.ui.statusbar.addWidget(main_obj.ui.status_spacer, stretch=1) 

        elif action == 'destruct':
            # Remove progress bar and label from status bar
            main_obj.ui.statusbar.removeWidget(main_obj.ui.progress)
            main_obj.ui.statusbar.removeWidget(main_obj.ui.status_label)
            main_obj.ui.statusbar.removeWidget(main_obj.ui.status_spacer)

            # Delete references
            # del main_obj.ui.progress
            # del main_obj.ui.status_label
            # del main_obj.ui.status_spacer        

class msg:
    @staticmethod    
    def show(main_obj, text, color="green", duration=4000):
        """Show message and then fade it out"""

        # Cancel any running animation first
        if hasattr(main_obj, "_fade_anim"):
            main_obj._fade_anim.stop()
            msg.clear_fading_components(main_obj)

        #Create components
        # Create a label inside the status bar
        main_obj.ui.status_label = QLabel("")
        main_obj.ui.status_label.setMinimumWidth(400)   
        main_obj.ui.status_label.setStyleSheet(f"color: {color};")         
        main_obj.ui.statusbar.addWidget(main_obj.ui.status_label)                

        #extra spacer to push prior items to left
        main_obj.ui.status_spacer = QWidget()    
        main_obj.ui.statusbar.addWidget(main_obj.ui.status_spacer, stretch=1)             

        # Fade in instantly, stay, then fade out
        main_obj.effect = QGraphicsOpacityEffect()     
        main_obj.ui.status_label.setGraphicsEffect(main_obj.effect)

        main_obj._fade_anim = QPropertyAnimation(main_obj.ui.status_label.graphicsEffect(), b"opacity")
        main_obj._fade_anim.setDuration(duration)
        main_obj._fade_anim.setEasingCurve(QEasingCurve.InCubic)        
        main_obj._fade_anim.setStartValue(1)          
        main_obj._fade_anim.setEndValue(0)        

        #Create fading text
        main_obj.ui.status_label.setText(text)        
        main_obj._fade_anim.start()    

        main_obj._fade_anim.finished.connect(lambda: msg.clear_fading_components(main_obj))

    @staticmethod 
    def clear_fading_components(main_obj):
        # Remove progress bar and label from status bar
        main_obj.ui.statusbar.removeWidget(main_obj.ui.status_label)
        main_obj.ui.statusbar.removeWidget(main_obj.ui.status_spacer)