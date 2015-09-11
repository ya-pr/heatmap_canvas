img = new Image();
img.src = "./img/palettes/color-5-red-02.png";

var vM, v0, pixPalette; //максимальное отклонение
vM = 75;
v0 = 1;
vM -= v0;


function calcColor(v, c) {
    if (v < 0) v = 0;
    if (v > 1) v = 1;
    return pixPalette[Math.floor((img.width - 1) * v) * 4 + c];
}

function calcData(i) {
    var color = i % 4,
        v;
    v = data[(i - color) / 4];
    v = (v - v0) / vM;
    if (color == 3) //прозрачность
    {
        if ((data[(i - color) / 4] == 0)) return 0;
        return 255;
    }
    return calcColor(v, color); //красный не используем вообще
}

window.addEventListener('load', function() {
    //загружаем палитру
    var canvasPalette = document.createElement('canvas');
    canvasPalette.width = img.width;
    canvasPalette.height = img.height;

    // Get the canvas 2d context.
    var contextPalette = canvasPalette.getContext('2d');
    if (!contextPalette || !contextPalette.getImageData || !contextPalette.putImageData || !contextPalette.drawImage) {
        alert(2);
        return;
    }
    contextPalette.drawImage(img, 0, 0);

    // Создадим объект ImageData.
    var imgdPalette = contextPalette.getImageData(0, 0, canvasPalette.width, canvasPalette.height);
    pixPalette = imgdPalette.data;

    //готовим область рисования
    document.getElementById('main').innerHTML = "<canvas width=" + x + " height=" + y + " id='myCanvas'>Your browser does not have support for Canvas</canvas>";
    var elem = document.getElementById('myCanvas');
    if (!elem || !elem.getContext) {
        alert(1);
        return;
    }

    // Get the canvas 2d context.
    var context = elem.getContext('2d');
    if (!context || !context.getImageData || !context.putImageData || !context.drawImage) {
        alert(2);
        return;
    }

    // Создадим объект ImageData.
    var imgd = context.createImageData(x, y);
    var pix = imgd.data;

    // Пройдемся по всем пикселям и зададим полупрозрачный красный цвет
    for (var i = 0; n = pix.length, i < n; i += 1) {
        pix[i] = calcData(i); // red channel
        //pix[i+1] = calcData(i/4,1); // red channel
        //pix[i+2] = 80; // red channel
        //pix[i+3] = 255; // alpha channel
    }

    // Отрисовать объект ImageData в заданных координатах (x,y).
    context.putImageData(imgd, 0, 0);

}, false);
