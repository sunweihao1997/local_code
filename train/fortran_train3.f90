program compute_sine
    implicit none
    real, parameter :: pi = 3.14159265
    integer, parameter :: n = 10
    real :: result_sin(n)
    integer :: i
  
    ! 并行循环，计算正弦值
    do concurrent (i = 1:n)
      result_sin(i) = sin(i * pi / 4.)
    end do
  
    ! 输出结果
    print *, result_sin
  
  end program compute_sine
  