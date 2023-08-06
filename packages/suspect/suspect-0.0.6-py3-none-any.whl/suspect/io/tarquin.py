def save_dpt(filename, data):
    with open(filename, 'wb') as fout:
        fout.write("Dangerplot_version\t1.0\n".encode())
        fout.write("Number_of_points\t{}\n".format(data.np).encode())
        fout.write("Sampling_frequency\t{0:8.8e}\n".format(1.0 / data.dt).encode())
        fout.write("Transmitter_frequency\t{0:8.8e}\n".format(data.f0 * 1e6).encode())
        fout.write("Phi0\t{0:8.8e}\n".format(0).encode())
        fout.write("Phi1\t{0:8.8e}\n".format(0).encode())
        fout.write("PPM_reference\t{0:8.8e}\n".format(data.ppm0).encode())
        fout.write("Echo_time\t{0:8.8e}\n".format(data.te).encode())
        fout.write("Real_FID\tImag_FID\t\n".encode())
        for x in data:
            fout.write("{0.real:8.8e} {0.imag:8.8e}\n".format(x).encode())