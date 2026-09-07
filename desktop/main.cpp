#include "browser_window.h"
#include <QApplication>
int main(int argc, char* argv[]) {
    QApplication app(argc, argv);
    app.setApplicationName("Carlinho Browser");
    app.setApplicationVersion(qEnvironmentVariable("CARLINHO_VERSION", "0.1.0"));
    BrowserWindow window; window.resize(1440,900); window.show();
    return app.exec();
}
