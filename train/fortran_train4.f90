program compute_sine_with_omp
    !use omp_lib  ! 使用 OpenMP 库
    implicit none
    real, parameter :: pi = 3.14159265
    integer, parameter :: n = 1000000
    real :: result_sin(n)
    integer :: i
    integer :: num_threads
  
    ! 获取 OpenMP 并行线程数量
    !num_threads = omp_get_max_threads()
    print *, "使用的线程数: ", num_threads
    
    !call system_clock(start_clock)
    ! 并行计算正弦值
    !do concurrent (i = 1:n)
    do i = 1,n
      result_sin(i) = sin(i * pi / 4.)
    end do
  
    ! 输出部分计算结果
    print *, "第一个计算结果: ", result_sin(1)
  
  end program compute_sine_with_omp
  