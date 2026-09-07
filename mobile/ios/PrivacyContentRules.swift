import WebKit

final class PrivacyContentRules {
    static func attach(to configuration: WKWebViewConfiguration, completion: @escaping (Error?) -> Void) {
        let rules = """
        [
          {"trigger":{"url-filter":".*doubleclick\\\\.net.*"},"action":{"type":"block"}},
          {"trigger":{"url-filter":".*google-analytics\\\\.com.*"},"action":{"type":"block"}},
          {"trigger":{"url-filter":".*googletagmanager\\\\.com.*"},"action":{"type":"block"}},
          {"trigger":{"url-filter":".*facebook\\\\.net.*"},"action":{"type":"block"}}
        ]
        """
        WKContentRuleListStore.default().compileContentRuleList(forIdentifier: "CarlinhoPrivacy", encodedContentRuleList: rules) { list,error in
            guard let list else { completion(error); return }
            configuration.userContentController.add(list); completion(nil)
        }
    }
}
