def create_tar(inputs=None, output=None):
    try:
        import tarfile

        with tarfile.open(output, "w:gz") as tar:
            for input_file in inputs:
                tar.add(input_file)
    except Exception as e:
        return str(e)
