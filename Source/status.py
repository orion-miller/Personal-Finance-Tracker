from PySide6.QtWidgets import (
    QWidget, 
    QGraphicsOpacityEffect,
    QLabel
)
from PySide6.QtCore import (
    QPropertyAnimation, QEasingCurve
)

class prog:
    def __init__(app):
        pass
    def update(app, msg, value):
        pass
    def close(app):
        pass

class msg:
    @staticmethod    
    def show(app, text, color="green", duration=4000):
        """Show message and then fade it out"""

        # Cancel any running animation first
        if hasattr(app, "_fade_anim"):
            app._fade_anim.stop()
            msg.clear_fading_components(app)

        #Create components
        # Create a label inside the status bar
        app.ui.status_label = QLabel("")
        app.ui.status_label.setMinimumWidth(400)   
        app.ui.status_label.setStyleSheet(f"color: {color};")         
        app.ui.statusbar.addWidget(app.ui.status_label)                

        #extra spacer to push prior items to left
        app.ui.status_spacer = QWidget()    
        app.ui.statusbar.addWidget(app.ui.status_spacer, stretch=1)             

        # Fade in instantly, stay, then fade out
        app.effect = QGraphicsOpacityEffect()     
        app.ui.status_label.setGraphicsEffect(app.effect)

        app._fade_anim = QPropertyAnimation(app.ui.status_label.graphicsEffect(), b"opacity")
        app._fade_anim.setDuration(duration)
        app._fade_anim.setEasingCurve(QEasingCurve.InCubic)        
        app._fade_anim.setStartValue(1)          
        app._fade_anim.setEndValue(0)        

        #Create fading text
        app.ui.status_label.setText(text)        
        app._fade_anim.start()    

        app._fade_anim.finished.connect(lambda: msg.clear_fading_components(app))

    @staticmethod 
    def clear_fading_components(app):
        # Remove progress bar and label from status bar
        app.ui.statusbar.removeWidget(app.ui.status_label)
        app.ui.statusbar.removeWidget(app.ui.status_spacer)