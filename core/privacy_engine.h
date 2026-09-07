#pragma once
#include <string>
#include <string_view>
#include <unordered_set>

namespace carlinho {
class PrivacyEngine final {
public:
    explicit PrivacyEngine(std::unordered_set<std::string> blocked_hosts = {});
    bool should_block_host(std::string_view host) const;
    bool is_third_party(std::string_view top_level_host, std::string_view request_host) const;
private:
    std::unordered_set<std::string> blocked_hosts_;
};
}
