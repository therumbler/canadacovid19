(function () {
    var data;
    var controls = document.querySelector('#controls');
    var totalPopulationElement = document.querySelector('#totalPopulation');
    var casesElement = document.querySelector('#cases');
    var rateElement = document.querySelector('#rate');

    function getRegionValue(id) {
        if (!id) {
            return;
        }
        var provinceName = id.substr(0, id.indexOf('-'));
        var regionName = id.substr(id.indexOf('-') + 1);
        // console.log('provinceName', provinceName, 'regionName', regionName)
        var resp;
        data.forEach(function (value) {
            for (const pn in value) {
                if (pn == provinceName) {
                    // console.log('provinceName', pn);
                    province = value[pn];
                    for (const rn in province) {
                        if (rn == regionName) {
                            resp = province[rn]
                        }
                    }
                }
            }
        });

        return resp;
    }
    function updateData() {
        var totalPopulation = 0;
        var totalCases = 0;
        var checkboxes = document.querySelectorAll('input[type=checkbox]');
        // console.log('checkboxes = ', checkboxes)

        checkboxes.forEach(function (checkbox) {
            // console.log(checkbox.checked);
            if (checkbox.checked) {
                var regionValue = getRegionValue(checkbox.id);
                if (!regionValue) {
                    return;
                }
                // console.log('regoinValue', regionValue);
                if (regionValue.population) {
                    totalPopulation = totalPopulation + parseInt(regionValue.population);
                    totalCases = totalCases + parseInt(regionValue.count);
                } else {
                    console.error('population is invalid', regionValue.population);
                }
            }
        });
        var rate = (totalCases / totalPopulation) * 100000;
        console.log('totalPopulation', totalPopulation, 'totalCases', totalCases);
        console.log('rate = ', rate);

        totalPopulationElement.innerHTML = totalPopulation;
        rateElement.innerHTML = rate;
        casesElement.innerHTML = totalCases;

        // for (checkbox in checkboxes) {
        //     console.log(checkbox);
        //     if (checkbox.value) {
        //         console.log(checkbox.id, 'is enabled')
        //     }

        // }
    }
    function createCheckbox(provinceName, regionName) {
        var id = provinceName + '-' + regionName;
        var checkbox = document.createElement('input');
        checkbox.setAttribute('type', 'checkbox');
        checkbox.setAttribute('name', id)
        checkbox.setAttribute('id', id)
        checkbox.setAttribute('checked', true);
        checkbox.addEventListener('change', updateData)
        checkbox.setAttribute('x-province', provinceName);
        controls.appendChild(checkbox);
        var label = document.createElement('label')
        label.innerHTML = regionName
        label.setAttribute('for', id);
        controls.append(label);
        // return checkbox;
    }
    function provinceSelection(evt) {
        var element = evt.target;
        var provinceName = element.getAttribute('x-province');
        console.log('provinceName', provinceName);
        var checkboxes = document.querySelectorAll('input[x-province="' + provinceName + '"]');
        checkboxes.forEach(function (checkbox) {
            checkbox.checked = element.checked;
        });
        updateData();
    }
    function createProvinceControls(province) {
        for (const provinceName in province) {
            // console.log('provinceName', provinceName);
            var checkbox = document.createElement('input');
            checkbox.setAttribute('type', 'checkbox');
            checkbox.setAttribute('x-province', provinceName);
            checkbox.addEventListener('change', provinceSelection);
            checkbox.setAttribute('checked', true);
            var h3 = document.createElement('h3');
            h3.innerHTML = provinceName;
            h3.appendChild(checkbox);
            controls.appendChild(h3);
            regions = province[provinceName]
            for (const regionName in regions) {
                createCheckbox(provinceName, regionName)

            }
        }
    }
    function createControls(data) {

        data.forEach(function (province) {
            // console.log(province);
            createProvinceControls(province);
        })
    }
    async function init() {
        var resp = await fetch('alldata.json');
        data = await resp.json()
        // console.log(data);
        createControls(data);
        updateData();
    }
    init();
})();