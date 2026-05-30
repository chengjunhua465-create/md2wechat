#!/usr/bin/env python3
"""Resume Builder v1.0 - Generate beautiful HTML resumes from JSON."""
import json, argparse, os, sys, webbrowser, tempfile

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{name} - Resume</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;background:#f0f2f5;color:#333;line-height:1.6;padding:20px}}
.resume{{max-width:800px;margin:0 auto;background:#fff;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,0.1);overflow:hidden}}
.header{{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:40px;text-align:center}}
.header h1{{font-size:32px;margin-bottom:8px}}
.header .title{{font-size:18px;opacity:0.9}}
.contact{{display:flex;justify-content:center;gap:20px;margin-top:15px;font-size:14px;flex-wrap:wrap}}
.section{{padding:25px 40px;border-bottom:1px solid #eee}}
.section h2{{font-size:18px;color:#667eea;margin-bottom:15px;padding-bottom:8px;border-bottom:2px solid #667eea}}
.skills{{display:flex;flex-wrap:wrap;gap:8px}}
.skill-tag{{background:#f0f2ff;color:#667eea;padding:4px 12px;border-radius:15px;font-size:13px;border:1px solid #d0d5ff}}
.item{{margin-bottom:20px}}
.item-header{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:5px}}
.item-header h3{{font-size:16px;color:#333}}
.item-header .period{{font-size:13px;color:#999}}
.item li{{font-size:14px;color:#555;margin-bottom:4px}}
@media print{{body{{background:#fff;padding:0}}.resume{{box-shadow:none;border-radius:0}}}}
</style></head>
<body><div class="resume">
<div class="header">
<h1>{name}</h1>
<div class="title">{title}</div>
<div class="contact"><span>&#x2709; {email}</span><span>&#x1F4F1; {phone}</span><span>&#x1F4CD; {location}</span></div>
</div>
{body}
</div></body></html>"""

SEC = '<div class="section"><h2>{title}</h2>{content}</div>'

def build(data):
    body = ""
    if data.get("summary"):
        body += SEC.format(title="&#x1F4CB; Summary", content='<div style="font-size:14px;color:#666;line-height:1.8">' + data["summary"] + '</div>')
    if data.get("skills"):
        tags = "".join('<span class="skill-tag">' + s + '</span>' for s in data["skills"])
        body += SEC.format(title="&#x1F527; Skills", content='<div class="skills">' + tags + '</div>')
    if data.get("experience"):
        items = ""
        for e in data["experience"]:
            highlights = "".join("<li>" + h + "</li>" for h in e.get("highlights", []))
            items += '<div class="item"><div class="item-header"><h3>' + e["company"] + '</h3><span class="period">' + e["period"] + '</span></div><div style="color:#667eea;font-size:14px;margin-bottom:8px">' + e["title"] + '</div><ul>' + highlights + '</ul></div>'
        body += SEC.format(title="&#x1F4BC; Experience", content=items)
    if data.get("education"):
        items = "".join('<div class="item"><div class="item-header"><h3>' + e["school"] + '</h3><span class="period">' + e["period"] + '</span></div><div style="color:#667eea;font-size:14px">' + e["degree"] + '</div></div>' for e in data["education"])
        body += SEC.format(title="&#x1F393; Education", content=items)
    if data.get("projects"):
        items = "".join('<div class="item"><h3>' + p["name"] + '</h3><div style="font-size:14px;color:#666">' + p["description"] + '</div><div style="font-size:12px;color:#999;margin-top:4px">&#x1F6E0; ' + p["tech"] + '</div></div>' for p in data["projects"])
        body += SEC.format(title="&#x1F680; Projects", content=items)
    return TEMPLATE.format(name=data.get("name",""), title=data.get("title",""), email=data.get("email",""), phone=data.get("phone",""), location=data.get("location",""), body=body)

def main():
    ap = argparse.ArgumentParser(description="Resume Builder - Generate HTML resumes")
    ap.add_argument("input", help="JSON resume file")
    ap.add_argument("-o","--output", help="Output HTML file")
    ap.add_argument("--preview", action="store_true", help="Preview in browser")
    ap.add_argument("--example", action="store_true", help="Generate example JSON")
    args = ap.parse_args()
    if args.example:
        ex = {"name":"Zhang San","title":"Senior Backend Engineer","email":"zhang@example.com","phone":"138-0000-0000","location":"Beijing","summary":"8 years experience in backend development and distributed systems.","skills":["Python","Java","Go","Docker","K8s","MySQL","Redis"],"experience":[{"company":"Tech Corp","period":"2020-present","title":"Senior Engineer","highlights":["Led core system redesign, 300% QPS improvement","Managed 5-person team"]}],"education":[{"school":"University","degree":"CS Bachelor","period":"2012-2016"}],"projects":[{"name":"Task Scheduler","description":"High-availability distributed task scheduler","tech":"Python/Redis/Kafka"}]}
        with open("resume.json","w",encoding="utf-8") as f: json.dump(ex,f,ensure_ascii=False,indent=2)
        print("Created resume.json example")
        return
    with open(args.input,encoding="utf-8") as f: data = json.load(f)
    html = build(data)
    if args.output:
        with open(args.output,"w",encoding="utf-8") as f: f.write(html)
        print("Saved to " + args.output)
    if args.preview:
        p = args.output
        if not p:
            tmp = tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8")
            tmp.write(html)
            tmp.close()
            p = tmp.name
        webbrowser.open("file://" + os.path.abspath(p))
    if not args.output and not args.preview:
        print(html)

if __name__ == "__main__":
    main()
