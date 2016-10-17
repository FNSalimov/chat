from PyQt4 import QtGui, QtCore
import design, sys, socket
from threading import Thread

class App(QtGui.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.setupUi(self)
        self.my_name = ''
        self.cli_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cli_socket.connect(('localhost', 5000))
        self.username()
        self.new_thread = Thread(target=self.handler)
        self.new_thread.start()
        #self.names = Thread(target=self.for_names)
        #self.names.start()
        self.lineEdit.setFocus(True)
        self.textEdit.setReadOnly(True)
        self.pushButton.clicked.connect(self.send)
    #def for_names(self):
    #    while 1:
    #        nam = self.cli_socket.rec
    def handler(self):
        while 1:
            #print(new_thread.is_alive())
            if not self.new_thread.is_alive():
                break
            rec_data = self.cli_socket.recv(1024).decode()
            #rec_data = rec_data.decode()
            if rec_data[0] + rec_data[1] == '->':
                if rec_data[2:] != self.my_name:
                    self.listWidget.addItem(rec_data[2:])
            #if not rec_data:
            #    breaks
            else:
                self.textEdit.append(rec_data)
            #print(rec_data.decode())
        self.cli_socket.close()
    def username(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Text Input Dialog', 'Enter your name:')
        if text and ok:
            self.my_name = str(text)
            self.cli_socket.send(self.my_name.encode())
            self.listWidget.addItem(text)
        else:
            self.username()
    def send(self):
        if self.lineEdit.text():
            mess = str(self.lineEdit.text())
            self.cli_socket.send(mess.encode())
            self.textEdit.append('you: ' + self.lineEdit.text())
        self.lineEdit.clear()
    def keyPressEvent(self, event):
        if event.key() == 16777220:
            self.send()
'''
def handler():
    while 1:
        a = input('you:\n')
        if not a:
            break
        cli_socket.send(a.encode())
'''
#if __name__ == '__main__':
app = QtGui.QApplication(sys.argv)
my_app = App()
my_app.show()

#user_name = input('your nickname: ')




sys.exit(app.exec_())
