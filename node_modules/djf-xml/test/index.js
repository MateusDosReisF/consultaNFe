var assert = require('assert')
var XmlParse = require('../src')

function fixture () {
  return '<service>test</service><item id="1">first</item><item id="2">second</item><user role="developer"><name>djf</name></user><similar><pFCPSTRet>1.0001</pFCPSTRet><pFCPST>1.0000</pFCPST></similar>'
}

describe('Examples', function () {
  it('should test examples', function () {
    var xml = XmlParse(fixture())

    // by tag
    // console.log(xml.tagValue('service')) // test
    assert.strictEqual(xml.tagValue('service'), 'test')

    // by tag and attribute
    // console.log(xml.tagValue('user', 'role')) // developer
    assert.strictEqual(xml.tagValue('user', 'role'), 'developer')

    // by nested tags
    // console.log(xml.tagValue('user').tagValue('name')) // djf
    assert.strictEqual(xml.tagValue('user').tagValue('name'), 'djf')

    // by array of tags, matching the first tag found
    // console.log(xml.tagValue(['not', 'service'])) // test
    assert.strictEqual(xml.tagValue(['not', 'service']), 'test')

    // group of tags
    var itens = xml.tagGroup('item')
    // console.log(itens) // ["<item id=\"1\">first</item>", "<item id=\"2\">second</item>"]
    // console.log(xml.tagValue('item', 'id')) // 1
    assert.strictEqual(itens.length, 2)
    assert.strictEqual(xml.tagValue('item', 'id'), '1')
  })
})

describe('Tests', function () {
  describe('invalidXML', function () {
    it('should test for invalid XML input', function () {
      assert.strictEqual(typeof XmlParse({}), 'object')

      assert.strictEqual(typeof XmlParse([]), 'object')

      assert.strictEqual(typeof XmlParse(null), 'object')

      assert.strictEqual(typeof XmlParse(), 'object')

      assert.strictEqual(typeof XmlParse(''), 'object')

      assert.strictEqual(typeof XmlParse(5), 'object')
    })
  })

  describe('tagValue', function () {
    it('should test tagValue()', function () {
      var xml = XmlParse(fixture())

      assert.strictEqual(xml.tagValue('service'), 'test')

      assert.strictEqual(xml.tagValue(['service']), 'test')

      assert.strictEqual(xml.tagValue(['not', 'service']), 'test')

      assert.strictEqual(xml.tagValue('user', 'role'), 'developer')

      assert.strictEqual(typeof xml.tagValue('user'), 'object')
    })
  })

  describe('invalidTagValue', function () {
    it('should test for invalid tagValue() args', function () {
      var xml = XmlParse(fixture())

      assert.strictEqual(xml.tagValue(), null)

      assert.strictEqual(xml.tagValue(''), null)

      assert.strictEqual(xml.tagValue(null), null)
    })
  })

  describe('tagGroup', function () {
    it('should test for tagGroup()', function () {
      var xml = XmlParse(fixture())

      var itens = xml.tagGroup('item')

      assert.strictEqual(itens.length, 2)
    })
  })

  describe('invalidTagGroup', function () {
    it('should test for invalid tagGroup() args', function () {
      var xml = XmlParse(fixture())

      assert.strictEqual(xml.tagGroup('notfound').length, 0)

      assert.strictEqual(xml.tagGroup().length, 0)

      assert.strictEqual(xml.tagGroup('').length, 0)

      assert.strictEqual(xml.tagGroup(null).length, 0)
    })
  })

  describe('similarTagName', function () {
    it('should test for similar tag names', function () {
      var xml = XmlParse(fixture())
      var similar = xml.tagValue('similar')

      assert.strictEqual(typeof similar, 'object')

      assert.strictEqual(similar.tagValue('pFCPST'), '1.0000')

      assert.strictEqual(similar.tagValue('pFCPSTRet'), '1.0001')
    })
  })
})
