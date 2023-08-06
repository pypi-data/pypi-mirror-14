
class AlignColumn(object):
    def __init__(self):
        self.m = 0
        self.m2 = 0
        self.mmax = 0
        self.mmin = 0

class Align(object):
    def __init__(self):

    def apply(self, strings):


    private function pickSizes(t: Table) {
        var w : Int = t.width;
        var h : Int = t.height;
        var v : View = t.getCellView();
        var csv  = new Csv();
        var sizes = new Array<Int>();
        var row = -1;
        var total = w-1; // account for commas
        for (x in 0...w) {
            var m : Float = 0;
            var m2 : Float = 0;
            var mmax : Int = 0;
            var mmostmax : Int = 0;
            var mmin : Int = -1;
            for (y in 0...h) {
                var txt = getText(x,y,false);
                if (txt=="@@"&&row==-1) {
                    row = y;
                }
                var len = txt.length;
                if (y==row) {
                    mmin = len;
                }
                m += len;
                m2 += len*len;
                if (len>mmax) mmax = len;
            }
            var mean = m/h;
            var stddev = Math.sqrt((m2/h)-mean*mean);
            var most = Std.int(mean+stddev*2+0.5);
            for (y in 0...h) {
                var txt = getText(x,y,false);
                var len = txt.length;
                if (len<=most) {
                    if (len>mmostmax) mmostmax = len;
                }
            }
            var full = mmax;
            most = mmostmax;
            if (mmin!=-1) {
                if (most<mmin) most = mmin;
            }
            if (wide_columns) {
                most = full;
            }
            sizes.push(most);
            total += most;
        }
        if (total>130) {  // arbitrary wide terminal size
            return null;
        }
        return sizes;
    }
