'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('django_admin_log', {
    'object_id': {
      type: DataTypes.STRING,
    },
    'object_repr': {
      type: DataTypes.STRING,
    },
    'action_flag': {
      type: DataTypes.INTEGER,
    },
    'change_message': {
      type: DataTypes.STRING,
    },
    'content_type_id': {
      type: DataTypes.INTEGER,
    },
    'user_id': {
      type: DataTypes.INTEGER,
    },
  }, {
    tableName: 'django_admin_log',
    underscored: true,
    timestamps: false,
    
  });

  Model.associate = (models) => {
  };

  return Model;
};

