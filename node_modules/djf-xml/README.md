# djf-xml
[![Build Status](https://travis-ci.org/djalmaoliveira/djf-xml.svg?branch=master)](https://travis-ci.org/djalmaoliveira/djf-xml)
[![Version](https://img.shields.io/npm/v/djf-xml.svg)](https://www.npmjs.com/package/djf-xml)

Simple javascript xml parser.

## Get started

### Installation

```
npm install djf-xml
```

### Usage
```javascript
var XmlParse = require('djf-xml')
function fixture () {
    return '<service>test</service><item id="1">first</item><item id="2">second</item><user role="developer"><name>djf</name></user>'
}

var xml = XmlParse(fixture())
// by tag
console.log(xml.tagValue('service')) // test

// by tag and attribute
console.log(xml.tagValue('user', 'role')) // developer

// by nested tags
console.log(xml.tagValue('user').tagValue('name')) // djf

// by array of tags, matiching the first tag found
console.log(xml.tagValue(['not', 'service'])) // test

// group of tags
var itens = xml.tagGroup('item')
console.log(itens) // ["<item id=\"1\">first</item>", "<item id=\"2\">second</item>"]
console.log(xml.tagValue('item', 'id')) // 1
```

## API Documentation

* __tagValue(tag, [attribute])__ - Return tag/attribute value or new Object.
    * param: tag - String or Array of tags, matching the first tag found.
    * param: attribute - String.

* __tagGroup(tag)__ - Return array of tags.
    * param: tag - String.

## Contributing

* [Please send pull request with tests.](https://github.com/djalmaoliveira/djf-xml/pulls)

### Running tests

```
npm run test
```

### Coding style

* [standardjs](https://standardjs.com/rules.html)


## Version

[Semantic Versioning](http://semver.org/)


## License

[MIT](https://github.com/djalmaoliveira/djf-xml/blob/master/LICENSE)
