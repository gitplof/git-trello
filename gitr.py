# -*- coding: utf-8 -*-
#!/usr/bin/python
import os
import re
import sys
import time
import json
import shutil
import logging

from optparse import OptionParser
from os.path import expanduser, join, realpath, isfile, dirname
from subprocess import check_call, CalledProcessError
from trello import TrelloClient

FORMAT = '%(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

try:
    from git import Repo
except ImportError as exc:
    logging.error("Failed to import settings module ({})".format(exc))
    logging.info("pip install gitpython") 
    sys.exit(2)

def get_short_id(string):
    short_id = string.split('#')
    ret = None

    if (len(short_id) > 1):
        digit = short_id[1]

        if digit.isdigit():
            ret = int(digit)

    return ret

def get_card_by_id(listr, short_id):
    cards = listr.list_cards()
    
    for card in cards:
        card.fetch()
        if (card.short_id == short_id):
            break
    else:
        return None

    return card

def checkout_by_id(repo, short_id, branch_type='F'):
    branch_id = "%c-#%d" % (branch_type, short_id)

    try:
        repo.remotes.origin.fetch()
    except AssertionError:
        pass

    if (branch_id == repo.active_branch.name):
        return

    for head in repo.heads:
        if (head.name == branch_id):
            head.checkout()
            break
    else:
        repo.active_branch.checkout(b=branch_id)

def check_untracked(repo):
    if repo.untracked_files:
        logging.warning('Commit your changes before checkout')
        sys.exit(2)

def git_add_commit(repo, msg):
    index = repo.index
    index.add(repo.untracked_files)
    index.add([diff.a_blob.name for diff in index.diff(None)])
    index.commit(message=msg)

def get_current_card(repo, listr):
    short_id = get_short_id(repo.active_branch.name)

    if short_id:
        card = get_card_by_id(listr, short_id)

    if not (short_id and card):
        handle_error('Your current branch (%s) has not target in list %s'\
         % (repo.active_branch.name, listr.name))

    return card

def handle_error(msg="", handle=logging, exit=True):
    handle.error(msg)
    if exit: sys.exit(2)


def check_params(params):
    params = params.split(',')

    for idx, digit in enumerate(params):
        if not digit.isdigit():
            handle_error('(-option <d1, d2, d3>) digits specified are wrong.')
        else:
            params[idx] = int(digit)

    return params

def main():
    usage = '%prog (load|rebuild|commit|push|test|config|update)'\
            ' [options] args... are you ready?'
    
    parser = OptionParser(usage)

    parser.add_option('-i', '--id',
                      type='int',
                      dest='id')

    parser.add_option('-u', '--user',
                      dest='user')

    parser.add_option('-c', '--comment',
                      dest='comment')

    parser.add_option('-g', '--gitpath',
                      default=realpath(__file__), 
                      dest='gitpath')

    parser.add_option('-p', '--params',
                      dest='params')

    parser.add_option('-t', '--title',
                      dest='title')

    parser.add_option('-d', '--description',
                      dest='description',
                      default="")

    (options, args) = parser.parse_args()

    repo = Repo(options.gitpath)
    conf_path = join(expanduser("~"), '.gitr.json')
    
    if not len(args):
        handle_error(msg='Some action are required', handle=parser)

    if not isfile(conf_path):
        conf_src = join(dirname(realpath(__file__)), 'gitr.json')
        shutil.copy(conf_src, conf_path)

    with open(conf_path, 'r') as infile:
        json_data = json.load(infile)

    BOARD_ID = json_data['BOARD_ID']
    CREATE_LIST_ID = json_data['CREATE_LIST_ID']
    DONE_LIST_ID = json_data['DONE_LIST_ID']
    MEMBERS = json_data['MEMBERS']
    USER = MEMBERS[int(json_data['USER'])]

    client = TrelloClient(api_key=json_data['API_KEY'], 
                          token=json_data['TOKEN'], 
                          api_secret=json_data['API_SECRET'])
    
    if ('update' in args):
        create_list = client.get_list(CREATE_LIST_ID)
        card = get_current_card(repo, create_list)

        if options.description:
            card._set_remote_attribute('description', options.description)

        if options.title or options.params:

            def sub_match(match):
                match_args = [arg for arg in match.groups()]

                if options.title:
                    match_args[4] = options.title

                if options.params:
                    params = check_params(options.params)

                    if (len(params) > 2):
                        match_args[2] = params[2]

                    elif (len(params) == 2):
                        match_args[1] = params[1]
                    
                    match_args[3] = params[0]

                return '#%s. %sº (%s,%s) %s' % tuple(match_args)

            name = re.sub('#(\d+).(\d+)º \((\d+),(\d+)\) (.*)', sub_match, card.name)
            card._set_remote_attribute('name', name)

    elif ('members' in args):
        for idx, member_id in enumerate(MEMBERS):
            member = client.get_member(member_id)

            logging.info("*%s %d. %s (%s)" % ((USER == member_id) and '*' or '', 
                idx, member.username, member.full_name))

    elif ('config' in args):
        if options.params:
            params = options.params.split(',')

            for param in params:
                try:
                    key, value = param.split(':')
                except ValueError:
                    handle_error('(-p <key:value, key2:value2, ...>)'\
                                 ' format is wrong.')
                json_data[key] = value

        if options.user:
            json_data['USER'] = options.user

        if not (options.params and options.user):
            members = client.get_board_members(BOARD_ID)
            json_data['MEMBERS'] = [member['id'] for member in members]
            json_data['USER'] = json_data['MEMBERS'].index(client.me()['id'])

        with open(conf_path, 'w') as outfile:
          json.dump(json_data, outfile)
        
        for key, value in json_data.items():
            logging.info("* %s: %s" %(key, value))

    elif ('load' in args):
        if not options.params:
            handle_error('(-p <t_estimated>)You must include '\
                         'almost time estimated.')

        params = check_params(options.params)
        (t_estimated, priority, t_real) = (params + [1, 0])[:3]

        if options.id:
            short_id = options.id
            create_list = client.get_list(CREATE_LIST_ID)
            card = get_card_by_id(create_list, short_id)

            if not card:
                handle_error('Card not found')

            full_title = '%dº (%d,%d) %s' % (priority, t_estimated, 
                                             t_real, card.name)
            
            card._set_remote_attribute('name', "#%d.%s" % (short_id, full_title))
            checkout_by_id(repo, short_id)

        else:
            if not options.title:
                handle_error('(-t <title>) to load is required')

            full_title = '%dº (%d,%d) %s' % (priority, t_estimated, 
                                             t_real, options.title)
            check_untracked(repo)
            create_list = client.get_list(CREATE_LIST_ID)
            card = create_list.add_card(full_title, options.description)

            if options.user:
                users = check_params(options.user)

                for member_pos in users:
                    member_id = MEMBERS[member_pos]
                    if (member_id <> USER):
                        card.assign(member_id)

            card.assign(USER)
            card.fetch()
            short_id = int(card.short_id)
            card._set_remote_attribute('name', "#%d.%s" % (short_id, card.name))
            checkout_by_id(repo, short_id)

    elif ('commit' in args):
        create_list = client.get_list(CREATE_LIST_ID)
        card = get_current_card(repo, create_list)

        if not options.comment:
            handle_error('(-c <comment>) to commit is required')

        card.comment(options.comment)
        git_add_commit(repo, options.comment)

    elif ('push' in args):
        create_list = client.get_list(CREATE_LIST_ID)
        card = get_current_card(repo, create_list)
        message = "CLOSED AT %s.\n%s" % (time.strftime('%Y-%m-%d %H:%M'), 
                                         options.comment or "")

        git_add_commit(repo, message)
        card.comment(message)
        card.change_list(DONE_LIST_ID)

        try:
            repo.remotes.origin.pull()
        except CalledProcessError:
            pass
        
        active_branch = repo.active_branch.name
        
        repo.remotes.origin.push()
        repo.heads.devel.checkout()
        check_call(('git', 'merge', active_branch))

    elif ('rebuild' in args):
        done_list = client.get_list(DONE_LIST_ID)
        card = get_current_card(repo, done_list)

    else:
        create_list = client.get_list(CREATE_LIST_ID)
        card = get_current_card(repo, create_list)
        message = "TESTED AT %s.\n%s" % (time.strftime('%Y-%m-%d %H:%M'), 
                                         options.comment or "")
        git_add_commit(repo, message)

        repo.heads.devel.checkout()
        repo.remotes.origin.pull()
        checkout_by_id(repo, card.short_id, 'I')

        try:
            check_call(('git', 'merge', 'F-#%d' % card.short_id))
        except CalledProcessError as error:
            handle_error('Conflict merge.')
        else:
            try:
                git_add_commit(repo, 'merge devel - I-#%d' % card.short_id)
            except CalledProcessError as error:
                handle_error(error)


if __name__ == '__main__':
    main()

