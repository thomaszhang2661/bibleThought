# 创世记研究笔记

## 目录1
```dataview
TABLE WITHOUT ID
    file.path AS "章节"
FROM "/"
WHERE file.name != this.file.name
    AND file.name != "index"
    AND !contains(file.path, "_attachments")
FLATTEN choice(
    contains(file.folder, ". "),
    number(split(file.folder, ". ")[0]),
    null
) AS folderOrder
FLATTEN choice(
    folderOrder != null,
    folderOrder,
    number(split(file.name, ". ")[0])
) AS orderKey
SORT orderKey ASC, file.path ASC
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






```dataview
TABLE WITHOUT ID
    "- [" + file.name + "](" + file.folder + "/" + file.name + ".md)" AS "章节"
FROM "/"
WHERE file.name != this.file.name
    AND file.name != "index"
    AND !contains(file.path, "_attachments")
SORT file.path ASC

```