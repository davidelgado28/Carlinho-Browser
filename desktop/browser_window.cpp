#include "browser_window.h"
#include "../core/privacy_engine.h"
#include <QAction>
#include <QLineEdit>
#include <QShortcut>
#include <QTabWidget>
#include <QToolBar>
#include <QUrl>
#include <QWebEnginePage>
#include <QWebEngineProfile>
#include <QWebEngineSettings>
#include <QWebEngineUrlRequestInterceptor>
#include <QWebEngineView>

namespace {
class PrivacyInterceptor final : public QWebEngineUrlRequestInterceptor {
public:
    explicit PrivacyInterceptor(QObject* parent=nullptr)
      : QWebEngineUrlRequestInterceptor(parent), engine_({
          "doubleclick.net","googletagmanager.com","google-analytics.com",
          "facebook.net","connect.facebook.net"}) {}
    void interceptRequest(QWebEngineUrlRequestInfo& info) override {
        if (engine_.should_block_host(info.requestUrl().host().toStdString())) info.block(true);
    }
private: carlinho::PrivacyEngine engine_;
};
static QString home_html() {
    return R"HTML(<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Carlinho Browser</title><style>
html,body{height:100%;margin:0;background:#000}body{display:grid;place-items:center;color:#fff;font-family:system-ui,sans-serif;background:radial-gradient(circle at center,#4d0009 0,#140000 28%,#000 66%)}
.logo{width:150px;height:150px;border-radius:50%;display:grid;place-items:center;background:#d40018;color:#fff;font-size:104px;font-weight:800;box-shadow:0 0 90px rgba(212,0,24,.33)}
</style></head><body><div class="logo">C</div></body></html>)HTML";
}
}
BrowserWindow::BrowserWindow(QWidget* parent):QMainWindow(parent){
    create_ui();
    profile_=new QWebEngineProfile(this);
    profile_->setHttpCacheType(QWebEngineProfile::MemoryHttpCache);
    profile_->setPersistentCookiesPolicy(QWebEngineProfile::NoPersistentCookies);
    profile_->setUrlRequestInterceptor(new PrivacyInterceptor(profile_));
    add_tab();
}
void BrowserWindow::create_ui(){
    setStyleSheet(R"(QMainWindow,QWidget,QToolBar,QTabWidget,QTabBar::tab{background:#050505;color:#f5f5f5}QLineEdit{background:#111;color:#fff;border:1px solid #262626;border-radius:10px;padding:8px 12px}QTabBar::tab{padding:8px 16px;margin:2px}QTabBar::tab:selected{background:#1b0006})");
    auto* toolbar=addToolBar("Navigation"); toolbar->setMovable(false);
    auto* back=toolbar->addAction("←"); auto* forward=toolbar->addAction("→"); auto* reload=toolbar->addAction("⟳"); toolbar->addSeparator();
    address_bar_=new QLineEdit(this); address_bar_->setPlaceholderText("Pesquisar ou digitar endereço"); toolbar->addWidget(address_bar_);
    tabs_=new QTabWidget(this); tabs_->setTabsClosable(true); tabs_->setDocumentMode(true); setCentralWidget(tabs_);
    connect(address_bar_,&QLineEdit::returnPressed,this,&BrowserWindow::navigate_current);
    connect(back,&QAction::triggered,this,[this]{if(auto* v=current_view())v->back();});
    connect(forward,&QAction::triggered,this,[this]{if(auto* v=current_view())v->forward();});
    connect(reload,&QAction::triggered,this,[this]{if(auto* v=current_view())v->reload();});
    connect(tabs_,&QTabWidget::tabCloseRequested,this,[this](int i){if(tabs_->count()>1)tabs_->widget(i)->deleteLater();});
    new QShortcut(QKeySequence("Ctrl+T"),this,[this]{add_tab();});
    new QShortcut(QKeySequence("Ctrl+W"),this,[this]{if(tabs_->count()>1)tabs_->widget(tabs_->currentIndex())->deleteLater();});
    new QShortcut(QKeySequence("Ctrl+R"),this,[this]{if(auto* v=current_view())v->reload();});
    new QShortcut(QKeySequence("F5"),this,[this]{if(auto* v=current_view())v->reload();});
    new QShortcut(QKeySequence("Ctrl+L"),this,[this]{focus_address_bar();});
    new QShortcut(QKeySequence("Ctrl+Tab"),this,[this]{if(tabs_->count())tabs_->setCurrentIndex((tabs_->currentIndex()+1)%tabs_->count());});
    new QShortcut(QKeySequence("Ctrl+Shift+Tab"),this,[this]{if(!tabs_->count())return;tabs_->setCurrentIndex((tabs_->currentIndex()-1+tabs_->count())%tabs_->count());});
}
void BrowserWindow::add_tab(){
    auto* view=new QWebEngineView(this); auto* page=new QWebEnginePage(profile_,view); view->setPage(page);
    view->settings()->setAttribute(QWebEngineSettings::JavascriptCanOpenWindows,false);
    view->setHtml(home_html(),QUrl("https://home.carlinho.local/"));
    const int index=tabs_->addTab(view,"Nova aba"); tabs_->setCurrentIndex(index);
    connect(view,&QWebEngineView::titleChanged,this,[this,view](const QString& title){int i=tabs_->indexOf(view);if(i>=0)tabs_->setTabText(i,title.left(32));});
    connect(view,&QWebEngineView::urlChanged,this,[this](const QUrl& url){if(!url.host().isEmpty())address_bar_->setText(url.toString());});
}
QWebEngineView* BrowserWindow::current_view() const { return qobject_cast<QWebEngineView*>(tabs_->currentWidget()); }
void BrowserWindow::navigate_current(){const auto text=address_bar_->text().trimmed();if(text.isEmpty())return;if(auto* v=current_view())v->setUrl(QUrl::fromUserInput(text));}
void BrowserWindow::focus_address_bar(){address_bar_->setFocus();address_bar_->selectAll();}
