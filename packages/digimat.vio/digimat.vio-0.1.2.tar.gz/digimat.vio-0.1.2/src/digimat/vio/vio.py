import time
from threading import RLock

# Easing functions
# pip import pytweening
import pytweening


class VIO(object):
    def __init__(self, name, initValue=0):
        self._lock=RLock()
        self._name=name
        self._value=self._normalizeInput(initValue)
        self._vioChild=None
        self._stamp=time.time()
        self._timeout=0
        self._reached=False
        self._pending=False

    @property
    def name(self):
        return self._name

    def chain(self, vio):
        if isinstance(vio, VIO):
            self._vioChild=vio
            print "chained"

    @property
    def value(self):
        with self._lock:
            self._manager()
            rvalue=self._value
            self._onValueSignaled(rvalue)
            return rvalue

    @value.setter
    def value(self, value):
        with self._lock:
            value=self._processInput(self._normalizeInput(value))
            if value!=self._value:
                self._processOutput(value)

    def reached(self):
        with self._lock:
            return bool(self._reached)

    def pending(self):
        with self._lock:
            return bool(self._pending)

    def age(self):
        return time.time()-self._stamp

    def _setTimeout(self, delay):
        with self._lock:
            self._timeout=time.time()+delay

    def _clearTimer(self):
            self._setTimeout(0)

    def _isTimeout(self):
        with self._lock:
            return time.time()>=self._timeout

    def valuestr(self):
        return '%.01f' % float(self._value)

    def __repr__(self):
        rstr='%s:%s:%s' % (type(self).__name__, self._name, self.valuestr())
        if self._vioChild is not None:
            rstr += "<-" + str(self._vioChild)
        return rstr

    def _normalizeInputBool(self, value):
        return bool(value)

    def _normalizeInput01(self, value):
        value=self._normalizeInputBool(value)
        if value:
            return 1
        return 0

    def _normalizeInput(self, value):
        return value

    def _processInputDenyUpdate(self, value):
        return self._value

    def _processInput(self, value):
        return value

    def _normalizeOutput(self, value):
        return value

    def _processOutput(self, value, reached=False):
        value=self._normalizeOutput(value)
        if value!=self._value:
            self._pending=True
            self._value=value
            self._stamp=time.time()
        if reached:
            self._reached=True

    def _manager(self):
        print "VIO:manager()"
        if self._vioChild is not None:
            self._vioChild._manager()
            self.value=self._vioChild.value

    def _onValueSignaled(self, value):
        pass


class VDout(VIO):
    def __init__(self, name, t01=0, t10=0, initValue=0):
        super(VDout, self).__init__(name, initValue)
        self._t01=float(t01)
        self._t10=float(t10)
        self._targetValue=self._value

    def _normalizeInput(self, value):
        return self._normalizeInput01(value)

    def _normalizeOutput(self, value):
        return self._normalizeInput01(value)

    def _processInput(self, value):
        if value!=self._targetValue:
            self._reached=False
            self._targetValue=value
            if value:
                self._setTimeout(self._t01)
            else:
                self._setTimeout(self._t10)
        return self._value

        def _manager(self):
            super(VDout, self)._manager()
            if not self._reached():
                print "VDout:manager()"
                if self._isTimeout():
                    self._processOutput(self._targetValue, True)


class Impulse(VIO):
    def __init__(self, name, delay):
        super(Impulse, self).__init__(name)
        self._delay=float(delay)
        self._targetValue=self._value

    def _normalizeInput(self, value):
        return self._normalizeInput01(value)

    def _normalizeOutput(self, value):
        return self._normalizeInput01(value)

    def _processInput(self, value):
        if value:
            self._reached=False
            self._setTimeout(self._delay)
            return 1
        return self._value

    def _manager(self):
        super(Impulse, self)._manager()
        if not self._reached:
            print "Impulse:manager()"
            if self._value:
                if self._isTimeout():
                    self._processOutput(0, True)

    def pulse(self):
        self.value=1

    def reset(self):
        self.value=0


class Oscillator(VIO):
    def __init__(self, name, t0, t1=0):
        super(Oscillator, self).__init__(name)
        self._t0=float(t0)
        if t1<=0:
            t1=t0
        self._t1=float(t1)
        self._reached=False

    def _normalizeInput(self, value):
        return self._normalizeInput01(value)

    def _normalizeOutput(self, value):
        return self._normalizeInput01(value)

    # neutralize value setter
    def _processInput(self, value):
        return self._processInputDenyUpdate(value)

    def _manager(self):
        super(Oscillator, self)._manager()
        if not self._reached:
            if self._isTimeout():
                if self._value:
                    self._processOutput(0)
                    self._setTimeout(self._t0)
                else:
                    self._processOutput(1)
                    self._setTimeout(self._t1)

    def start(self):
        self._reached=False

    def stop(self):
        self._processOutput(0, True)
        self._clearTimer()


class RisingEdge(VIO):
    def __init__(self, name):
        super(RisingEdge, self).__init__(name)

    def _normalizeInput(self, value):
        return self._normalizeInput01(value)

    def _normalizeOutput(self, value):
        return self._normalizeInput01(value)

    def _processInput(self, value):
        if value:
            return self._value+1
        return self._value

    def _onValueSignaled(self, value):
        self._processOutput(0)


class Edge(VIO):
    def __init__(self, name):
        super(Edge, self).__init__(name)
        self._rawValue=0

    def _normalizeInput(self, value):
        return self._normalizeInput01(value)

    def _normalizeOutput(self, value):
        return self._normalizeInput01(value)

    def _processInput(self, value):
        if value!=self._rawValue:
            self._rawValue=value
            return self._value+1
        return self._value

    def _onValueSignaled(self, value):
        self._processOutput(0)


class DInverter(VIO):
    def __init__(self, name):
        super(DInverter, self).__init__(name)
        self._rawValue=0

    def _normalizeInput(self, value):
        return self._normalizeInput01(value)

    def _normalizeOutput(self, value):
        return self._normalizeInput01(value)

    def _processInput(self, value):
        if value!=self._rawValue:
            self._rawValue=value
            if value:
                return not bool(self._value)
        return self._value


class VAout(VIO):
    def __init__(self, name, rateUpPerSecond=0, rateDownPerSecond=0, initValue=0):
        super(VAout, self).__init__(name, initValue)
        self._rateUpPerSecond=float(rateUpPerSecond)
        self._rateDownPerSecond=float(rateDownPerSecond)
        self._targetValue=self._value
        self._stampUpdate=0

    def _normalizeInput(self, value):
        return float(value)

    def _normalizeOutput(self, value):
        return float(value)

    def _processInput(self, value):
        if value!=self._targetValue:
            self._reached=False
            self._targetValue=value
            self._stampUpdate=time.time()
        return self._value

    def _manager(self):
        super(VAout, self)._manager()
        if not self._reached:
            print "VAout:manager()"
            dt=time.time()-self._stampUpdate
            self._stampUpdate=time.time()
            if self._targetValue>self._value:
                if self._rateUpPerSecond>0:
                    self._value+=self._rateUpPerSecond*dt
                    if self._value>self._targetValue:
                        self._processOutput(self._targetValue, True)
                else:
                    self._processOutput(self._targetValue, True)
            else:
                if self._rateDownPerSecond>0:
                    self._value-=self._rateDownPerSecond*dt
                    if self._value<self._targetValue:
                        self._processOutput(self._targetValue, True)
                else:
                    self._processOutput(self._targetValue, True)


class AFilterEasing(VIO):
    def __init__(self, name, T=5.0, easing=None, initValue=0):
        super(AFilterEasing, self).__init__(name, initValue)
        self._T=float(T)
        if self._T<0:
            self._T=0.0
        self._targetValue=self._value
        self._startValue=self._value
        self._stampUpdate=0
        self._easing=easing
        if not self._easing:
            self._easing=pytweening.easeOutQuad

    def easing(self, f):
        # seee http://easings.net/fr for easing description
        self._easing=f

    def _normalizeInput(self, value):
        return float(value)

    def _normalizeOutput(self, value):
        return float(value)

    def _processInput(self, value):
        if value!=self._targetValue:
            self._reached=False
            self._targetValue=value
            self._startValue=self._value
            self._stampUpdate=time.time()
        return self._value

    def _manager(self):
        super(AFilterEasing, self)._manager()
        print "AFilter:manager()"
        if not self._reached:
            dt=time.time()-self._stampUpdate
            try:
                ease=self._easing(dt/self._T)
                self._processOutput(self._startValue+ease*(self._targetValue-self._startValue))
            except:
                self._processOutput(self._targetValue, True)


class AFilterEaseOutQuad(AFilterEasing):
    def __init__(self, name, T=5.0, initValue=0):
            super(AFilterEaseOutQuad, self).__init__(name, T, pytweening.easeOutQuad, initValue)


class AFilterEaseInQuad(AFilterEasing):
    def __init__(self, name, T=5.0, initValue=0):
            super(AFilterEaseInQuad, self).__init__(name, T, pytweening.easeInQuad, initValue)


# class Chenillard(VIO):
#       def __init__(self, name, size, delay=1):
#               super(Chenillard, self).__init__(name)
#               if isinstance(size, (list, tuple)):
#                       self._items=size
#                       self._size=len(size)
#               else:
#                       self._items=None
#                       self._size=size
#               self._delay=delay
#               self._loop=0
#               self._value=-1

#       def __getitem__(self, i):
#               with self._lock:
#                       self._manager()
#                       if i>=0 and i<self._size and self._value==int(i):
#                               return 1
#                       return 0

#       def channels(self):
#               with self._lock:
#                       self._manager()
#                       values=[0 for x in range(self._size)]
#                       if self.isActive():
#                               values[self._value]=1
#                       return values

#       def items(self):
#               return self._items

#       def itemActive(self):
#               try:
#                       with self._lock:
#                               self._manager()
#                               if self.isActive() and self._items:
#                                       return self._items[self._value]
#               except:
#                       pass

#       def __repr__(self):
#               return str(self.channels())

#       def _manager(self):
#               if self.isActive() and self._isTimeout():
#                       self._value+=1
#                       if self._value<self._size:
#                               self._setTimeout(self._delay)
#                       else:
#                               if self._loop>0:
#                                       self._loop-=1
#                                       self._value=0
#                                       self._setTimeout(self._delay)
#                               else:
#                                       self._value=-1

#       def _processInput(self, value):
#               return self._value

#       def start(self, count=1):
#               with self._lock:
#                       if count>0:
#                               self._loop=count-1
#                               self._value=0
#                               self._setTimeout(self._delay)
#                       else:
#                               self.stop()

#       def isActive(self):
#               return self._value>=0

#       def stop(self):
#               with self._lock:
#                       self._loop=0
#                       self._value=-1


class VIOCollection(object):
    def __init__(self, name=None):
        self._name=name
        self._vios={}

    @property
    def name(self):
        return self._name

    def get(self, name):
        try:
            return self._vios[name]
        except:
            pass

    def __getitem__(self, name):
        try:
            return self.get(name)
        except:
            pass

    def add(self, vio):
        if vio is not None and isinstance(vio, VIO):
            if not self.get(vio.name):
                self._vios[vio.name]=vio
                return vio

    def vios(self):
        return self._vios.values()

    def manager(self):
        for vio in self.vios():
            vio.value
