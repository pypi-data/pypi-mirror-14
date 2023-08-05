from __future__ import division, print_function
import numpy as np



class Tsintegrator(object):
    """
    Super class for the the integration via Tanh-Sinh quadrature.
    """

    def __init__(self,N=20,hstep=3.15):
        """
        :param N:  Precision number, the number of functional evaluation is equal to
                   Nf=2N+1.
        :param hstep: Step for the integration.
        NB, Caveat: The routines will calculate positions using the value of hstep. It can be possible
        that float has not enough precision to properly store the final values and the extreme points can be equal
        to the integration extrema. This can be a problem if you are integrating function with some problems at the
        extrema. To overcome this problem we can pass perform the integration between -1 and 1 and/or lower the hstep.
        :return:
        """

        self.N=N
        self.hstep=hstep
        self.pimezzi=0.5*np.pi

    def _generateGen(self,N,hstep):
        """
        Generate positions and weights between -1 and 1.
        :param N:
        :param hstep:
        :return:
        """
        N=int(N)
        h=hstep/N
        kh=np.arange(-N,N+1)*h

        return self._generateX(kh),self._generateW(kh,h)

    def _generateW(self,t,h):
        """
        Generate weigths  in the  range -11
        :param t: arg (k*h)
        :return:
        """

        den=np.cosh(self.pimezzi*np.sinh(t))

        return  h*( self.pimezzi*np.cosh(t) ) / (  den*den )

    def _generateX(self,t):
        """
        Generate positions for a range -11
        :param t: arg
        :return:
        """

        return np.tanh(  self.pimezzi * np.sinh(t)   )

    def _generateAB(self,x,w,a,b):
        """
        Convert Xp and Wp for integration between a and b
        :param a: Limite inf
        :param b: Limite sup
        :return: new xp and wp
        """
        a=float(a)
        b=float(b)
        c2=(b+a)/(b-a)
        if b!=0.: c1=b/(c2+1)
        else: c1=a/(c2-1)


        xpn=c1*(x+c2)
        wpn=c1*w

        return xpn,wpn

class Tsintegrator1D(Tsintegrator):

    def __init__(self,N=20,hstep=3.15):
        """
        :param N:  Precision number, the number of functional evaluation is equal to
                   Nf=2N+1.
        :param hstep: Step for the integration.
        NB, Caveat: The routines will calculate positions using the value of hstep. It can be possible
        that float has not enough precision to properly store the final values and the extreme points can be equal
        to the integration extrema. This can be a problem if you are integrating function with some problems at the
        extrema. To overcome this problem we can pass perform the integration between -1 and 1 and/or lower the hstep.
        :return:
        """
        super(Tsintegrator1D, self).__init__(N,hstep)
        self.xp,self.wp=self._generate()

    def _generate(self):
        """
        Generate position and weights
        :return:
        """
        return self._generateGen(self.N,self.hstep)

    def integrate(self,func,a=-1,b=1):

        x,w=self._generateAB(self.xp,self.wp,a,b)

        if (x[-1]==b) or (x[0]==a):
            print('Warning one ox the extreme integration points is equal to the integral extrema')

        res=np.sum(w*func(x))

        return res

class Tsintegrator2D(Tsintegrator):
    def __init__(self,N=20,hstep=3.15):
        """
        :param N:  Precision number, the number of functional evaluation is equal to
                   Nf=2N+1. It can be a single number of a list with Nx and Ny.
        :param hstep: Step for the integration.
        NB, Caveat: The routines will calculate positions using the value of hstep. It can be possible
        that float has not enough precision to properly store the final values and the extreme points can be equal
        to the integration extrema. This can be a problem if you are integrating function with some problems at the
        extrema. To overcome this problem we can pass perform the integration between -1 and 1 and/or lower the hstep.
        :return:
        """
        if isinstance(N,int) or isinstance(N,float):
            super(Tsintegrator2D, self).__init__(N,hstep)
            self.xp,self.wpx=self._generate1D()
            self.yp=self.xp
            self.wpy=self.wpx
            self.check1d=True
        elif len(N)==1:
            super(Tsintegrator2D, self).__init__(N,hstep)
            self.N=N[0]
            self.xp,self.wpx=self._generate1D()
            self.yp=self.xp
            self.wpy=self.wpx
            self.check1d=True
        else:
            super(Tsintegrator2D, self).__init__(N,hstep)
            self.xp,self.wpx,self.yp,self.wpy= self._generate2D()
            self.check1d=False

    def _generate1D(self):
        """
        Generate position and weights if Nx=Ny
        :return:
        """
        return self._generateGen(self.N,self.hstep)

    def _generate2D(self):
        """
        Generate position and weights if Nx!=Ny
        :return:
        """
        x,wx=self._generateGen(self.N[0],self.hstep)
        y,wy=self._generateGen(self.N[1],self.hstep)

        return x,wx,y,wy

    def integrate(self,func,xlim=(-1,1),ylim=(-1,1)):

        x,wx=self._generateAB(self.xp,self.wpx,xlim[0],xlim[1])
        y,wy=self._generateAB(self.yp,self.wpy,ylim[0],ylim[1])

        if (x[-1]==xlim[-1]) or (x[0]==xlim[0]) or (y[0]==ylim[0]) or (y[-1]==ylim[-1]):
            print('Warning one ox the extreme integration points is equal to the integral extrema')

        xx,yy=np.meshgrid(x,y)
        wwx,wwy=np.meshgrid(wx,wy)

        res=np.sum(wwx*wwy*func(xx,yy))

        return res



