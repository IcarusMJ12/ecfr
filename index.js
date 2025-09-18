
// selecting a row in one of the tables should select corresponding rows in the
// other
let selected = false
const agency_title_map = new Map()
const title_agency_map = new Map()

const make_agency_row = (agency, table, is_child) => {
  const row = table.insertRow(-1)
  row.id = agency['hash']
  const hash = row.insertCell(0)
  const name = row.insertCell(1)
  const wc = row.insertCell(2)
  let ref1;if (is_child) { ref1 = ('<span style="color: white;">-</span> '
                                    + agency['hash'])} else ref1 = agency['hash'];hash.innerHTML = ref1
  name.innerHTML = agency['name']
  wc.innerHTML = agency['wc']
  agency_title_map.set(agency['hash'], agency['cfr_references'])
  const results=[];for (const cfr of agency['cfr_references']) {
    const key = 't' + cfr['title']
    const val = title_agency_map.get(key) || []
    val.push(row.id)
    results.push(title_agency_map.set(key, val))
  };return results;
}


$(document).ready(() => {
  return $.getJSON('payload.json', (payload) => {
    // populate agency table and agency to title selection mapping
    const agency_table = $('#agencies > tbody')[0]
    for (const agency of payload['agencies']) {
      make_agency_row(agency, agency_table)
      for (const child of agency['children']) {
        make_agency_row(child, agency_table, true)
      }
    }

    // populate title table and title to agency selection mapping
    const title_table = $('#titles > tbody')[0]
    for (const title of payload['titles']) {
      const row = title_table.insertRow(-1)
      row.id = 't' + title['number']
      const number = row.insertCell(0)
      const name = row.insertCell(1)
      const versions = row.insertCell(2)
      number.innerHTML = title['number']
      name.innerHTML = title['name']
      let results1="";for (const version of title['versions']) {
        results1 += `<a target='_blank' href='https://www.ecfr.gov/on/${version}/title-${title["number"]}'>${version}</a> `
      };versions.innerHTML = results1
    }

    // grey out agencies and non-matching titles on row click
    $('#agencies').on('click', 'tbody tr', (evt) => {
      if (selected && evt.currentTarget.className == '') {
        $('tbody > tr').removeClass('deselected')
        $('#refs').html('')
        selected = false
        return
      }

      $('tbody > tr').addClass('deselected')
      const titles = agency_title_map.get(evt.currentTarget.id)
      const refs = []
      for (const title of titles) {
        $('#t' + title['title']).removeClass('deselected')
        const ref = []
        for (const key in title) {const value = title[key];
          ref.push(`${key}: ${value}`)
        }
        refs.push(ref.join(', '))
      }
      evt.currentTarget.className = ''
      $('#refs').html(refs.join('<br>'))
      console.log(titles)
      console.log($('#refs'))
      return selected = true
    })

    // grey out titles and non-matching agencies on row click
    return $('#titles').on('click', 'tbody tr', (evt) => {
      // ignore links as they open a new page
      if (evt.target.tagName == 'A') {
        return
      }

      $('#refs').html('')

      if (selected && evt.currentTarget.className == '') {
        $('tbody > tr').removeClass('deselected')
        selected = false
        return
      }

      $('tbody > tr').addClass('deselected')
      const agencies = title_agency_map.get(evt.currentTarget.id)
      for (const agency of agencies) {
        $('#' + agency).removeClass('deselected')
      }
      evt.currentTarget.className = ''
      return selected = true
    })
  })
})
