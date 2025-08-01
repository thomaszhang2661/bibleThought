<style>
body {
  font-size: 24px;
  font-family: "Helvetica Neue", sans-serif;
  line-height: 1.8;
  padding: 40px;
  background-color: #f9f9f9;
  color: #222;
}

a {
  font-size: 20px;
  color: #007acc;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>

```dataview
TABLE WITHOUT ID
    "- [" + file.folder + "/" + file.name + "](" + file.path + ")" AS "章节"
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