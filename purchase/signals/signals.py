def temp_files_delete(sender, instance, **kwargs):
    instance.delete_temp_files()
