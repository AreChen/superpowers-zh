# GitHub issue

已安装并认证时使用 `gh`，由它处理认证、速率限制和 JSON。
否则依次回退到通过 curl 访问公开 API，以及交给人类伙伴打开的 URL。

## 搜索

```bash
gh search issues --repo obra/superpowers --limit 10 "<terms>" \
  --json number,state,title --jq '.[] | "\(.number)\t\(.state)\t\(.title)"'
```

没有 `gh` 时（未认证，每分钟 10 次请求）：

```bash
curl -s -H "Accept: application/vnd.github+json" \
  "https://api.github.com/search/issues?q=repo:obra/superpowers+is:issue+<url-encoded terms>&per_page=10" \
  | jq -r '.items[] | "\(.number)\t\(.state)\t\(.title)"'
```

没有 curl 时，提供 `https://github.com/obra/superpowers/issues?q=<terms>`。

## 提交

将填写好的 `templates/issue.md` 写入工作区，并展示完整原文。获批后：

```bash
gh issue create --repo obra/superpowers --title "<title>" --body-file <path> \
  --label bug --label automated-issue-report
```

报告者没有推送权限时，GitHub 会静默丢弃标签，因此只有协作者
提交时标签才会生效；模板页脚仍会注明该 issue 由技能生成。
`gh` 无法附加文件：issue 创建后，给人类伙伴诊断包路径，
让其通过浏览器附加。

没有 `gh` 时，提供使用 `diagnosis_report.md` 模板的预填链接；
该模板会为任何报告者应用这两个标签：

```
https://github.com/obra/superpowers/issues/new?template=diagnosis_report.md&title=<url-encoded title>&body=<url-encoded body>
```

GitHub 会拒绝长度超过约 8,000 个字符的 URL；超出时只在链接中
预填标题，并请人类伙伴从文件中粘贴正文。
