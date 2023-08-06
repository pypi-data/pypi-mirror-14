from inqbus.tagging.functions import add_tags, get_tagging_config, get_all_keywords


def title_to_tag(context, event):
    """
    Find keywords from the title of a content object. According to the configuration keywords may be added only, if they
    already exist, or new keywords may be generated from the title.
    :param context: The content object
    :return: Nothing
    """
    # get the tagging configuration
    tagging_config = get_tagging_config()

    # Check if the title has to used at all. If not do nothing
    if tagging_config.scan_title or tagging_config.new_tags_from_title:
        # get the title
        title = context.title

        # check if the title should be scanned and if a regex for scanning is provided
        if tagging_config.scan_title and tagging_config.scan_title_regex:
            # do the scanning
            title_tags = tagging_config.scan_title_regex_compiled.findall(title)
            # get a list a already existing keyowrds. TODO Optimization (caching, lower case matching, use sets or dicts)
            existing_keywords = get_all_keywords(context)
            # match the keywords to the exiting ones
            for tag in title_tags:
                if tag in existing_keywords:
                    # add the matching keywords
                    add_tags(context, tags_to_add=[tag])

        # check if the title should be scanned for new keywords and if a regex for the scanning is provided
        if tagging_config.new_tags_from_title and tagging_config.new_tags_from_title_regex:
            # do the scanning
            new_title_tags = tagging_config.new_tags_from_title_regex_compiled.findall(title)
            # TODO Optimization (caching, lower case matching, use sets or dicts)
            # add the keywords
            add_tags(context, tags_to_add=new_title_tags)


