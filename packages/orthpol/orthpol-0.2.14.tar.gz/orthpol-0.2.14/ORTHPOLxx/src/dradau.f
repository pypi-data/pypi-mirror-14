c
c
      subroutine dradau(n,dalpha,dbeta,dend,dzero,dweigh,ierr,de,
     *da,db)
c
c This is a double-precision version of the routine  radau.
c
      double precision dend,dp0,dp1,dpm1,dalpha(*),dbeta(*),
     *dzero(*),dweigh(*),de(*),da(*),db(*)
c
c The arrays  dalpha,dbeta,dzero,dweigh,de,da,db  are assumed to have
c dimension  n+1.
c
      np1=n+1
      do 10 k=1,np1
        da(k)=dalpha(k)
        db(k)=dbeta(k)
   10 continue
      dp0=0.d0
      dp1=1.d0
      do 20 k=1,n
        dpm1=dp0
        dp0=dp1
        dp1=(dend-da(k))*dp0-db(k)*dpm1
   20 continue
      da(np1)=dend-db(np1)*dp0/dp1
      call dgauss(np1,da,db,dzero,dweigh,ierr,de)
      return
      end

