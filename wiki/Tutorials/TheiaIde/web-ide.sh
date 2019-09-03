#!/bin/bash
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.5/install.sh | bash
nvm install 8
npm install -g yarn
mkdir IDE
cd IDE
cat > package.json << "END"
{
  "private": true,
  "dependencies": {
    "typescript": "latest",
    "@theia/typescript": "latest",
    "@theia/navigator": "latest",
    "@theia/terminal": "latest",
    "@theia/outline-view": "latest",
    "@theia/preferences": "latest",
    "@theia/messages": "latest",
    "@theia/git": "latest",
    "@theia/file-search": "latest",
    "@theia/markers": "latest",
    "@theia/preview": "latest",
    "@theia/callhierarchy": "latest",
    "@theia/merge-conflicts": "latest",
    "@theia/search-in-workspace": "latest",
    "@theia/json": "latest",
    "@theia/textmate-grammars": "latest",
    "@theia/mini-browser": "latest"
  },
  "devDependencies": {
    "@theia/cli": "latest"
  }
}
END
yarn
yarn theia build
