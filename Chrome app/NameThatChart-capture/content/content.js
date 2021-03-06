var jcrop, selection;

var overlay = ((active) => (state) => {
    active = (typeof state === 'boolean') ? state : (state === null) ? active : !active;
    $('.jcrop-holder')[active ? 'show' : 'hide']();
    chrome.runtime.sendMessage({message: 'active', active})
})(false);

var image = (done) => {
    var image = new Image();
    image.id = 'fake-image';
    image.src = chrome.runtime.getURL('/images/pixel.png');
    image.onload = () => {
        $('body').append(image);
        done()
    }
};

function dataURLtoBlob(dataurl) {
    var arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
    while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new Blob([u8arr], {type: mime});
}

var init = (done) => {
    $('#fake-image').Jcrop({
        bgColor: 'none',
        onSelect: (e) => {
            selection = e;
            capture()
        },
        onChange: (e) => {
            selection = e
        },
        onRelease: (e) => {
            setTimeout(() => {
                selection = null
            }, 100)
        }
    }, function ready() {
        jcrop = this;

        $('.jcrop-hline, .jcrop-vline').css({
            backgroundImage: 'url(' + chrome.runtime.getURL('/images/Jcrop.gif') + ')'
        });

        if (selection) {
            jcrop.setSelect([
                selection.x, selection.y,
                selection.x2, selection.y2
            ])
        }

        done && done()
    })
};

var capture = (force) => {
    chrome.storage.sync.get((config) => {
        if (selection && (config.method === 'crop' || (config.method === 'wait' && force))) {
            jcrop.release();
            setTimeout(() => {
                chrome.runtime.sendMessage({
                    message: 'capture', area: selection, dpr: devicePixelRatio
                }, (res) => {
                    overlay(false);
                    selection = null;
                    save(res.image)
                })
            }, 50)
        }
        else if (config.method === 'view') {
            chrome.runtime.sendMessage({
                message: 'capture',
                area: {x: 0, y: 0, w: innerWidth, h: innerHeight}, dpr: devicePixelRatio
            }, (res) => {
                overlay(false);
                save(res.image)
            })
        }
    })
};

var filename = () => {
    var pad = (n) => ((n = n + '') && (n.length >= 2 ? n : '0' + n));
    var timestamp = ((now) =>
    [pad(now.getFullYear()), pad(now.getMonth() + 1), pad(now.getDate())].join('-')
    + ' - ' +
    [pad(now.getHours()), pad(now.getMinutes()), pad(now.getSeconds())].join('-'))(new Date());
    return 'Screenshot Capture - ' + timestamp + '.png'
};


var save = (image) => {
    $("body").append("<div id='modolal33'><div id='modolal33-content'> <div id='modolal33-header'><span id='modolal33-close'>&times;</span> <h2 id='modolal33-mh'>Name That Chart app</h2> </div> <div id='modolal33-body'> </div> <div id='modolal33-footer'> <h3 id='modolal33-mf'>Keep your image id to trace it</h3> </div> </div> </div>");
    $("#modolal33").show();

    var modal = document.getElementById('modolal33');
    var span = document.getElementById("modolal33-close");
    $("#modolal33-body").empty();
    $("#modolal33-body").append("<img id='img' src='" + chrome.runtime.getURL('/images/loading.gif') + "'/>");
    span.onclick = function () {
        modal.style.display = "none";
        $("#modolal33-body")
    };
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
            $("#modolal33-body")
        }
    };
    var form = new FormData();
    form.append("local", dataURLtoBlob(image));

    var settings = {
        "async": true,
        "crossDomain": true,
        "url": "http://namethat-env.cfuws7rm8t.eu-west-1.elasticbeanstalk.com/saveapp",
        "method": "POST",
        "processData": false,
        "contentType": false,
        "mimeType": "multipart/form-data",
        "data": form
    };


    $.ajax(settings).done(function (response) {
        $("#img").hide();
        $("#modolal33-body").append(response);
    });
};

window.addEventListener('resize', ((timeout) => () => {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
        jcrop.destroy();
        init(() => overlay(null))
    }, 100)
})());

chrome.runtime.onMessage.addListener((req, sender, res) => {
    if (req.message === 'init') {
        res({});// prevent re-injecting

        if (!jcrop) {
            image(() => init(() => {
                overlay();
                capture()
            }))
        }
        else {
            overlay();
            capture(true)
        }
    }
    return true
});
