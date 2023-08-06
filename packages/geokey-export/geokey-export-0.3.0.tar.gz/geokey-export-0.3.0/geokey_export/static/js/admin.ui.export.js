/* ****************************************************************************
 * Listens for a change of selected project and gets
 * all categories of it.
 *
 * @author Patrick Rickles (p.rickles@ucl.ac.uk)
 * @author Julius Osokinas (j.osokinas@mappingforchange.org.uk)
 * ***************************************************************************/

$(function() {
    'use strict';

    var initialLoad = false;

    function populateContributions(contributions) {
        var geometry = $('#geometry').val();
        var length = 0;

        if (window.map && layer instanceof L.FeatureGroup && contributions) {
            L.geoJson(contributions, {
                onEachFeature: function() {
                    length++;
                }
            }).addTo(layer);

            if (length > 0) {
                if (initialLoad && geometry) {
                    return;
                } else {
                    window.map.fitBounds(layer.getBounds(), {
                        padding: [50, 50]
                    });
                }
            }
        }
    }

    var projectSelect = $('select[name=project]');
    var categorySelect = $('select[name=category]');
    var projectId, categoryId;

    projectSelect.on('change', function() {
        projectId = $(this).val();

        categorySelect.find('option').each(function() {
            if ($(this).val() !== '') {
                $(this).remove();
            }
        });

        if (projectId) {
            $.get('/admin/export/projects/' + projectId + '/categories/', function(categories) {
                if (categories) {
                    for (var key in categories) {
                        if (categories.hasOwnProperty(key)) {
                            categorySelect.append($('<option value="' + key + '">' + categories[key] + '</option>'));
                        }
                    }
                }
            });
        }

        categorySelect.parent().removeClass('hidden');

        if (layer instanceof L.FeatureGroup) {
            layer.clearLayers();
        }
    });

    categorySelect.on('change', function() {
        categoryId = $(this).val();

        if (layer instanceof L.FeatureGroup) {
            layer.clearLayers();
        }

        if (projectId && categoryId) {
            $.get('/admin/export/projects/' + projectId + '/categories/' + categoryId + '/contributions/', function(contributions) {
                populateContributions(contributions);
            });
        }
    });

    var layer = new L.FeatureGroup();

    if (window.map) {
        window.map.addLayer(layer);
    }

    var exportId = $('body').data('export');

    if (exportId) {
        initialLoad = true;

        $.get('/admin/export/' + exportId + '/contributions/', function(contributions) {
            populateContributions(contributions);
        });
    }
});
