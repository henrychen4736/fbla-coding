import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.12

ApplicationWindow {
    visible: true
    width: 400
    height: 300
    title: "Login Page"

    Rectangle {
        anchors.fill: parent
        color: "#f0f0f0"

        ColumnLayout {
            anchors.centerIn: parent
            spacing: 20

            TextField {
                id: usernameField
                placeholderText: "Username"
                Layout.preferredWidth: 200
            }

            TextField {
                id: passwordField
                placeholderText: "Password"
                echoMode: TextField.Password
                Layout.preferredWidth: 200
            }

            Button {
                id: loginButton
                text: "Log In"
                Layout.preferredWidth: 200
                onClicked: {
                    console.log("Login attempt with username: " + usernameField.text + " and password: " + passwordField.text)
                }
            }
        }
    }
}
