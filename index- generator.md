# 创世记研究笔记

## 目录1

```dataview
TABLE WITHOUT ID
    "- [" + file.folder + "/" + file.name + "](" + file.path + ")" AS "章节"
FROM "/"
WHERE file.name != this.file.name
    AND file.name != "index"
    AND !contains(file.path, "_attachments")
SORT file.path ASC
```

## 目录2




```dataview
TABLE WITHOUT ID
    "- [" + file.name + "](" + file.path + ")" AS "章节"
FROM "/"
WHERE file.name != this.file.name
      AND file.name != "index"
      AND !contains(file.path, "_attachments")
SORT file.name ASC
```