from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QIntValidator, QIcon
from PyQt6 import uic
import configparser
import threading
import send

class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('MainWindow.ui', self)
        self.show()
        
        self.setWindowIcon(QIcon('img\cattocry.png'))
        
        self.channelID.setValidator(QIntValidator(self))
        self.delay.setValidator(QIntValidator(self))
        self.randomDelayMIN.setValidator(QIntValidator(self))
        self.randomDelayMAX.setValidator(QIntValidator(self))

        self.startButton.clicked.connect(self.start_button)
        self.randomTimeCheckBox.toggled.connect(self.check)
        
        self.load_config()
        
    def check(self):    
        if self.randomTimeCheckBox.isChecked():
            self.delay.setEnabled(False)
            self.randomDelayMIN.setEnabled(True)
            self.randomDelayMAX.setEnabled(True)
            
            self.delay.setText('')
        else:
            self.delay.setEnabled(True)
            self.randomDelayMIN.setEnabled(False)
            self.randomDelayMAX.setEnabled(False)
            
            self.randomDelayMIN.setText('')
            self.randomDelayMAX.setText('')
        
    def load_config(self):
        config = configparser.ConfigParser()
        config.read_file(open(r'config.ini'))
        discord_token = config.get('Config', 'discord_token')
        warp_name = config.get('Config', 'warp_name')
        delay = config.get('Config', 'delay')
        MIN_delay = config.get('Config', 'MIN_delay')
        MAX_delay = config.get('Config', 'MAX_delay')
        channel_ID = config.get('Config', 'channel_ID')
        message_content = config.get('Config', 'message_content')
        
        delete_message = eval(config.get('Config', 'delete_message'))
        random_time = eval(config.get('Config', 'random_time'))
        notifications = eval(config.get('Config', 'notifications'))
            
        self.discordToken.setText(discord_token)
        self.warpName.setText(warp_name)
        self.delay.setText(delay)
        self.randomDelayMIN.setText(MIN_delay)
        self.randomDelayMAX.setText(MAX_delay)
        self.channelID.setText(channel_ID)
        self.messageContent.setText(message_content)
        
        self.deleteMessageCheckBox.setChecked(delete_message)
        self.randomTimeCheckBox.setChecked(random_time)
        self.notificationCheckBox.setChecked(notifications)
    
    def save_config(self):
        config = configparser.ConfigParser()
        config.add_section('Config')
        config.set('Config', 'discord_token', self.discordToken.text())
        config.set('Config', 'warp_name', self.warpName.text())
        config.set('Config', 'delay', self.delay.text())
        config.set('Config', 'MIN_delay', self.randomDelayMIN.text())
        config.set('Config', 'MAX_delay', self.randomDelayMAX.text())
        config.set('Config', 'channel_ID', self.channelID.text())
        config.set('Config', 'message_content', self.messageContent.toPlainText())
            
        config.set('Config', 'delete_message', str(self.deleteMessageCheckBox.isChecked()))
        config.set('Config', 'random_time', str(self.randomTimeCheckBox.isChecked()))
        config.set('Config', 'notifications', str(self.notificationCheckBox.isChecked()))
    
        with open('config.ini', 'w') as config_file:
            config.write(config_file)
        
    def start_button(self):
        self.save_config()      
        self.startButton.setEnabled(False)
        self.startButton.setText('by matswuuu')

        send_thread = threading.Thread(target=send.send, name='send_thread')
        if not send_thread.is_alive():
            send_thread.start()

    def closeEvent(self, event):
        self.save_config()
            
app = QApplication([])
UIWindow = Ui()
app.exec()