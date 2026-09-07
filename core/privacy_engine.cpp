#include "privacy_engine.h"
#include <algorithm>
#include <cctype>

namespace carlinho {
static std::string normalize(std::string_view host) {
    std::string out(host);
    std::transform(out.begin(), out.end(), out.begin(), [](unsigned char c){ return static_cast<char>(std::tolower(c)); });
    while (!out.empty() && out.front()=='.') out.erase(out.begin());
    while (!out.empty() && out.back()=='.') out.pop_back();
    return out;
}
PrivacyEngine::PrivacyEngine(std::unordered_set<std::string> blocked_hosts) {
    for (const auto& h : blocked_hosts) blocked_hosts_.insert(normalize(h));
}
bool PrivacyEngine::should_block_host(std::string_view host) const {
    const auto n = normalize(host);
    if (blocked_hosts_.contains(n)) return true;
    std::size_t dot = n.find('.');
    while (dot != std::string::npos) {
        if (blocked_hosts_.contains(n.substr(dot+1))) return true;
        dot = n.find('.', dot+1);
    }
    return false;
}
bool PrivacyEngine::is_third_party(std::string_view top_level_host, std::string_view request_host) const {
    const auto top = normalize(top_level_host);
    const auto req = normalize(request_host);
    if (top.empty() || req.empty() || top == req) return false;
    if (req.size() > top.size()) {
        const auto off = req.size() - top.size();
        if (req.compare(off, top.size(), top) == 0 && req[off-1]=='.') return false;
    }
    return true;
}
}
