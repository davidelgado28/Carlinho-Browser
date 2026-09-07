#pragma once
#include <QMainWindow>
class QLineEdit; class QTabWidget; class QWebEngineProfile; class QWebEngineView;
class BrowserWindow final : public QMainWindow {
    Q_OBJECT
public: explicit BrowserWindow(QWidget* parent=nullptr);
private:
    void create_ui(); void add_tab(); QWebEngineView* current_view() const;
    void navigate_current(); void focus_address_bar();
    QTabWidget* tabs_{nullptr}; QLineEdit* address_bar_{nullptr}; QWebEngineProfile* profile_{nullptr};
};
