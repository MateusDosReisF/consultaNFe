/**
 * Extract group of tags
 *
 * @param      {<string>}  xml      The xml
 * @param      {<string>}  tagName  The tag name
 */
function extractGroup (xml, tagName) {
  var itens = []
  var regex = new RegExp(`<${tagName}.+?>(.+?)</${tagName}>`, 'gi')
  var result = ''
  for (result = regex.exec(xml); regex.lastIndex !== 0; result = regex.exec(xml)) {
    itens.push(result[0])
  }

  return itens
}

/**
 * Extract value between tags.
 *
 * @param      {<string>}  xml      The xml
 * @param      {<string|array>}  tagName        The tag name
 * @param      {<string>}  attributeName  The attribute name
 * @return     {string | null}
 */
function extract (xml, tagName, attributeName) {
  if (!Array.isArray(tagName)) {
    tagName = [tagName]
  }

  var found = null
  var tagFound = null
  for (var i = 0; i < tagName.length; i++) {
    // without attributes
    found = new RegExp(`<${tagName[i]}\\s*>(.+?)</${tagName[i]}>`, 'i').exec(xml)
    if (found) {
      tagFound = tagName[i]
      break
    }

    // with attributes
    found = new RegExp(`<${tagName[i]} .*?>(.+?)</${tagName[i]}>`, 'i').exec(xml)
    if (found) {
      tagFound = tagName[i]
      break
    }
  }

  if (found && attributeName) {
    var attribute = new RegExp(`<${tagFound} .*?${attributeName}=\"(.+?)\".*?>`, 'i').exec(found[0])
    if (attribute) {
      return attribute[1]
    }
  }

  return found ? found[1] : null
}

/**
 * Determines if it has tags.
 *
 * @param      {<string>}   content  The content
 * @return     {boolean}  True if has tags, False otherwise.
 */
function hasTags (content) {
  return (content.split('</', 2)[0] !== content)
}

/**
 * Return the xml object model based on <xml> specified.
 *
 * @param      {string}  xml     The xml
 * @return     {Object}  {tagValue(), tagGroup()}
 */
function model (xml) {
  var path = ''
  var cache = {}
  xml = xml && typeof xml === 'string' ? xml.replace(/[\n\r]/gi, '') : ''

  return {
    tagValue: (tag, attribute) => {
      if (!Array.isArray(tag)) {
        tag = [tag]
      }

      path = tag.join('_') + '_' + (attribute || '')

      if (typeof cache[path] === 'undefined') {
        cache[path] = extract(xml, tag, attribute)
        if (typeof cache[path] === 'string' && hasTags(cache[path])) {
          cache[path] = model(cache[path])
        }
      }

      return cache[path]
    },
    tagGroup: (tag) => {
      return extractGroup(xml, tag)
    }
  }
}

module.exports = model
